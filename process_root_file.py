import os
import sys
import argparse
import itertools
from datetime import datetime

import numpy as np
from sqlalchemy.sql import exists
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

import ROOT
#import root_numpy as rnp

from guppy import hpy

import log
from classes import Histogram

from dqm.database import db_session
from dqm.models import DataQualityRun, DataQualitySubRun

# heapy
hp = hpy()

# argparse
parser = argparse.ArgumentParser(description="Analyze from ROOT file.")
parser.add_argument('file', type=str, help="path to ROOT file")
args = parser.parse_args()

# CAEN boards and channels
v1740_boards = xrange(0, 7+1)
v1751_boards = xrange(8, 9+1)
v1740b_boards = xrange(24, 24+1)
caen_boards = list(itertools.chain(v1740_boards, v1751_boards, v1740b_boards))

v1740_channels = xrange(64)
v1751_channels = xrange(8)
v1740b_channels = xrange(64)

# histogram names
pedestal_th1_name = "DataQuality/pedestal/caen_board_{}_channel_{}_pedestal"
adc_th1_name = "DataQuality/adc/caen_board_{}_channel_{}_adc"
ustof_hits_th1_name = "DataQuality/tof/USTOFHits"
dstof_hits_th1_name = "DataQuality/tof/DSTOFHits"
tof_th1_name = "DataQuality/tof/TOF"

# TTree names
event_record_ttree_name = "DataQuality/artEventRecord"
event_builder_ttree_name = "DataQuality/EventBuilderTree"
wut_ttree_name = "DataQuality/wut"

# load ROOT file
f = ROOT.TFile(args.file)

def get_mean_and_rms(boards, channels):
    """ Get mean and RMS from pedestal and ADC histograms. """
    pedestal_mean = []
    pedestal_rms = []
    pedestal_integral = []
    adc_mean = []
    adc_rms = []
    adc_integral = []
    for board in boards:
        pedestal_mean_ = []
        pedestal_rms_ = []
        pedestal_integral_ = []
        adc_mean_ = []
        adc_rms_ = []
        adc_integral_ = []
        for channel in channels:
            h_pedestal = f.Get(pedestal_th1_name.format(board, channel))
            h_adc = f.Get(adc_th1_name.format(board, channel))
            pedestal_mean_.append(h_pedestal.GetMean())
            pedestal_rms_.append(h_pedestal.GetRMS())
            pedestal_integral_.append(h_pedestal.Integral())
            adc_mean_.append(h_adc.GetMean())
            adc_rms_.append(h_adc.GetRMS())
            adc_integral_.append(h_adc.Integral())
        pedestal_mean.append(pedestal_mean_)
        pedestal_rms.append(pedestal_rms_)
        pedestal_integral.extend(list(set(pedestal_integral_)))
        adc_mean.append(adc_mean_)
        adc_rms.append(adc_rms_)
        adc_integral.extend(list(set(adc_integral_)))
    return pedestal_mean, pedestal_rms, adc_mean, adc_rms, \
           pedestal_integral, adc_integral

def histogram_arrays(th1):
    """ Get arrays from histogram. """
    bins = []
    counts = []
    number_bins = th1.GetNbinsX()
    for bin_index in xrange(number_bins):
        bins.append(th1.GetBin(bin_index))
        counts.append(th1.GetBinContent(bin_index))
    return np.array(bins), np.array(counts, dtype=np.int64)

# get run, sub-run, and time stamp from EventRecord TTree
event_record_ttree = f.Get(event_record_ttree_name)

run = 0
subrun = 0
timestamp = 0
event_record_read = False

for branch in event_record_ttree:
    run = branch.run_number
    subrun = branch.sub_run_number
    timestamp = branch.time_stamp_low
    event_record_read = True
    break

if not event_record_read:
    print "EventRecord TTree not read!"

count = DataQualitySubRun.query.filter_by(run=run, subrun=subrun).count()

# check if subrun exists in database
subrun_exists = db_session.query(exists()
                                 .where(DataQualitySubRun.run == run)
                                 .where(DataQualitySubRun.subrun == subrun)
                                ).scalar()

# if subrun exists in database, exit
if subrun_exists:
    db_session.close()  # close transaction
    sys.exit(1)

# EventBuilder TTree
event_builder_ttree = f.Get(event_builder_ttree_name)

# WUT TTree
wut_ttree = f.Get(wut_ttree_name)

# get number of events, TPC events, and data blocks
# get timestamps of data blocks
number_events = 0
number_tpc_events = 0

number_caen_data_blocks = { board : 0 for board in caen_boards }
number_tdc_data_blocks = 0
number_wut_data_blocks = 0

caen_timestamps = { board : [] for board in caen_boards }
tdc_timestamps = []
wut_timestamps = []

# loop over EventBuilder TTree
for branch in event_builder_ttree:
    number_events += 1
    number_tpc_events += branch.NumberTPCReadouts

    for board in caen_boards:
        number_caen_data_blocks[board] += getattr(
            branch, "NumberCAENBoard{}Blocks".format(board))
        caen_timestamps[board].extend(
            list(getattr(branch, "CAENBoard{}TimeStamps".format(board))))

    number_tdc_data_blocks += branch.NumberTDCBlocks
    tdc_timestamps.extend(list(branch.TDCTimeStamps))

# loop over WUT TTree
for branch in wut_ttree:
    number_wut_data_blocks += 1
    wut_timestamps.append(branch.time_header)

# get mean and RMS of pedestal and ADC histograms
v1740_pedestal_mean, v1740_pedestal_rms, v1740_adc_mean, v1740_adc_rms, \
v1740_pedestal_integral, v1740_adc_integral \
    = get_mean_and_rms(v1740_boards, v1740_channels)

v1751_pedestal_mean, v1751_pedestal_rms, v1751_adc_mean, v1751_adc_rms, \
v1751_pedestal_integral, v1751_adc_integral \
    = get_mean_and_rms(v1751_boards, v1751_channels)

v1740b_pedestal_mean, v1740b_pedestal_rms, v1740b_adc_mean, v1740b_adc_rms, \
v1740b_pedestal_integral, v1740b_adc_integral \
    = get_mean_and_rms(v1740b_boards, v1740b_channels)

#print v1740_pedestal_integral
#print v1740_adc_integral
#print v1751_pedestal_integral
#print v1751_adc_integral
#print v1740b_pedestal_integral
#print v1740b_adc_integral

# TPC pedestal/ADC mean and RMS
tpc_pedestal_mean = list(itertools.chain.from_iterable(v1740_pedestal_mean[:7]))
tpc_pedestal_mean.extend(v1740_pedestal_mean[7][:32])

tpc_pedestal_rms = list(itertools.chain.from_iterable(v1740_pedestal_rms[:7]))
tpc_pedestal_rms.extend(v1740_pedestal_rms[7][:32])

tpc_adc_mean = list(itertools.chain.from_iterable(v1740_adc_mean[:7]))
tpc_adc_mean.extend(v1740_adc_mean[7][:32])

tpc_adc_rms = list(itertools.chain.from_iterable(v1740_adc_rms[:7]))
tpc_adc_rms.extend(v1740_adc_rms[7][:32])

# get USTOF hits histogram
ustof_hits_th1 = f.Get(ustof_hits_th1_name)
ustof_hits_bins, ustof_hits_counts = histogram_arrays(ustof_hits_th1)
ustof_hits_histogram = Histogram("ustof_hits")
ustof_hits_histogram.histogram_to_db(ustof_hits_bins, ustof_hits_counts)

# get DSTOF hits histogram
dstof_hits_th1 = f.Get(dstof_hits_th1_name)
dstof_hits_bins, dstof_hits_counts = histogram_arrays(dstof_hits_th1)
dstof_hits_histogram = Histogram("dstof_hits")
dstof_hits_histogram.histogram_to_db(dstof_hits_bins, dstof_hits_counts)

# get TOF histogram
tof_th1 = f.Get(tof_th1_name)
tof_bins, tof_counts = histogram_arrays(tof_th1)
tof_histogram = Histogram("tof")
tof_histogram.histogram_to_db(tof_bins, tof_counts)

#print tof_histogram.bins_sparse
#print tof_histogram.counts_sparse

#print np.array(v1740_pedestal_mean).shape
#print np.array(v1740_pedestal_rms).shape
#print np.array(v1751_pedestal_mean).shape
#print np.array(v1751_pedestal_rms).shape
#print np.array(v1740b_pedestal_mean).shape
#print np.array(v1740b_pedestal_rms).shape

#print np.array(v1740_adc_mean).shape
#print np.array(v1740_adc_rms).shape
#print np.array(v1751_adc_mean).shape
#print np.array(v1751_adc_rms).shape
#print np.array(v1740b_adc_mean).shape
#print np.array(v1740b_adc_rms).shape

#print np.array(v1751_adc_mean)
#print np.array(v1751_adc_rms)

# convert time stamp to date time
date_time = datetime.fromtimestamp(timestamp)

# instantiate DataQualitySubRun
dqm_subrun = DataQualitySubRun(
    run=run, subrun=subrun, date_time=date_time,
    date_time_added=datetime.now())

db_session.close()

print hp.heap()

