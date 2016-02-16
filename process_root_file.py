#/////////////////////////////////////////////////////////////
# Name:      process_root_file.py
# Date:      14 February 2016
# Author:    Everybody is an author!
#/////////////////////////////////////////////////////////////

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

#/////////////////////////////////////////////////////////////
# heapy
#/////////////////////////////////////////////////////////////
hp = hpy()

#/////////////////////////////////////////////////////////////
# argparse
#/////////////////////////////////////////////////////////////
parser = argparse.ArgumentParser(description="Analyze from ROOT file.")
parser.add_argument('file', type=str, help="path to ROOT file")
args = parser.parse_args()

#/////////////////////////////////////////////////////////////
# iterators for CAEN boards and channels
#/////////////////////////////////////////////////////////////
v1740_boards = range(0, 7+1)
v1751_boards = range(8, 9+1)
v1740b_boards = range(24, 24+1)
caen_boards = list(itertools.chain(v1740_boards, v1751_boards, v1740b_boards))
non_tpc_caen_boards = sorted(list(set(caen_boards) - set(v1740_boards[:-1])))

v1740_channels = xrange(64)
v1751_channels = xrange(8)
v1740b_channels = xrange(64)

#/////////////////////////////////////////////////////////////
# histogram names
#/////////////////////////////////////////////////////////////
pedestal_th1_name = "DataQuality/pedestal/caen_board_{}_channel_{}_pedestal"
adc_th1_name = "DataQuality/adc/caen_board_{}_channel_{}_adc"
ustof_hits_th1_name = "DataQuality/tof/USTOFHits"
dstof_hits_th1_name = "DataQuality/tof/DSTOFHits"
tof_th1_name = "DataQuality/tof/TOF"

#/////////////////////////////////////////////////////////////
# TTree names
#/////////////////////////////////////////////////////////////
event_record_ttree_name = "DataQuality/artEventRecord"
event_builder_ttree_name = "DataQuality/EventBuilderTree"
wut_ttree_name = "DataQuality/wut"

#/////////////////////////////////////////////////////////////
# numpy histogram config for timestamps of data blocks
#/////////////////////////////////////////////////////////////
timestamps_bin_range = (0, 60)
timestamps_bins = 600

#/////////////////////////////////////////////////////////////
# load ROOT file
#/////////////////////////////////////////////////////////////
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

def th1_to_arrays(th1):
    """ Get arrays from histogram. """
    bins = []
    counts = []
    number_bins = th1.GetNbinsX()
    for bin_index in xrange(number_bins):
        bins.append(th1.GetBin(bin_index))
        counts.append(th1.GetBinContent(bin_index))
    return np.array(bins), np.array(counts, dtype=np.int64)

#/////////////////////////////////////////////////////////////
# get run, sub-run, and time stamp from EventRecord TTree
#/////////////////////////////////////////////////////////////
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

#/////////////////////////////////////////////////////////////
# check if subrun exists in database
#/////////////////////////////////////////////////////////////
subrun_exists = db_session.query(exists()
                                 .where(DataQualitySubRun.run == run)
                                 .where(DataQualitySubRun.subrun == subrun)
                                ).scalar()

# TODO: Check DataQualityRun to see if subrun had been added.

#/////////////////////////////////////////////////////////////
# if subrun exists in database, exit
#/////////////////////////////////////////////////////////////
if subrun_exists:
    print "Run {}, SubRun {} already exists in table!".format(run, subrun)
    print "Exiting..."
    db_session.close()  # close transaction
    sys.exit(1)

#/////////////////////////////////////////////////////////////
# check if run exists in database
#/////////////////////////////////////////////////////////////
run_exists = db_session.query(exists()
                              .where(DataQualityRun.run == run)
                             ).scalar()

# EventBuilder TTree
event_builder_ttree = f.Get(event_builder_ttree_name)

# WUT TTree
wut_ttree = f.Get(wut_ttree_name)

#/////////////////////////////////////////////////////////////
# get number of events, TPC events, and data blocks
# get timestamps of data blocks
#/////////////////////////////////////////////////////////////
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
            list(getattr(branch, "CAENBoard{}TimeStamps".format(board))))  # microseconds

    number_tdc_data_blocks += branch.NumberTDCBlocks
    tdc_timestamps.extend(list(branch.TDCTimeStamps))  # microseconds

# loop over WUT TTree
for branch in wut_ttree:
    number_wut_data_blocks += 1
    wut_timestamps.append(branch.time_header * 16e-6)  # seconds

#/////////////////////////////////////////////////////////////
# convert timestamps of data blocks from microseconds to seconds
#/////////////////////////////////////////////////////////////
for board in caen_boards:
    caen_timestamps[board] = [ x * 1e-6 for x in caen_timestamps[board] ]  # seconds
tdc_timestamps = [ x * 1e-6 for x in tdc_timestamps ]  # seconds

#/////////////////////////////////////////////////////////////
# histograms for timestamps of data blocks
#/////////////////////////////////////////////////////////////
caen_timestamps_counts = { board : [] for board in caen_boards }
caen_timestamps_bins = { board : [] for board in caen_boards }
caen_timestamps_histograms = {
    board : Histogram("caen_board_{}_timestamps".format(board))
    for board in caen_boards }

for board in caen_boards:
    # numpy histogram for CAEN timestamps
    caen_timestamps_counts[board], caen_timestamps_bins[board] = np.histogram(
        caen_timestamps[board],
        bins=timestamps_bins,
        range=timestamps_bin_range)
    caen_timestamps_bins[board] = caen_timestamps_bins[board][:-1]  # get rid of "overflow" bin

    # use Histogram class for CAEN timestamps
    caen_timestamps_histograms[board].histogram_to_db(
        caen_timestamps_bins[board], caen_timestamps_counts[board])

#/////////////////////////////////////////////////////////////
# numpy histogram for TDC timestamps
#/////////////////////////////////////////////////////////////
tdc_timestamps_counts, tdc_timestamps_bins = np.histogram(
    tdc_timestamps, bins=timestamps_bins, range=timestamps_bin_range)
tdc_timestamps_bins = tdc_timestamps_bins[:-1]  # get rid of "overflow" bin

#/////////////////////////////////////////////////////////////
# use Histogram class for TDC timestamps
#/////////////////////////////////////////////////////////////
tdc_timestamps_histogram = Histogram("tdc_timestamps")
tdc_timestamps_histogram.histogram_to_db(tdc_timestamps_bins,
                                         tdc_timestamps_counts)

#/////////////////////////////////////////////////////////////
# numpy histogram for WUT timestamps
#/////////////////////////////////////////////////////////////
wut_timestamps_counts, wut_timestamps_bins = np.histogram(
    wut_timestamps, bins=timestamps_bins, range=timestamps_bin_range)
wut_timestamps_bins = wut_timestamps_bins[:-1]  # get rid of "overflow" bin

#/////////////////////////////////////////////////////////////
# use Histogram class for WUT timestamps
#/////////////////////////////////////////////////////////////
wut_timestamps_histogram = Histogram("wut_timestamps")
wut_timestamps_histogram.histogram_to_db(wut_timestamps_bins,
                                         wut_timestamps_counts)

#/////////////////////////////////////////////////////////////
# get mean and RMS of pedestal and ADC histograms
#/////////////////////////////////////////////////////////////
v1740_pedestal_mean, v1740_pedestal_rms, v1740_adc_mean, v1740_adc_rms, \
v1740_pedestal_integral, v1740_adc_integral \
    = get_mean_and_rms(v1740_boards, v1740_channels)

v1751_pedestal_mean, v1751_pedestal_rms, v1751_adc_mean, v1751_adc_rms, \
v1751_pedestal_integral, v1751_adc_integral \
    = get_mean_and_rms(v1751_boards, v1751_channels)

v1740b_pedestal_mean, v1740b_pedestal_rms, v1740b_adc_mean, v1740b_adc_rms, \
v1740b_pedestal_integral, v1740b_adc_integral \
    = get_mean_and_rms(v1740b_boards, v1740b_channels)

#/////////////////////////////////////////////////////////////
# TPC pedestal/ADC mean and RMS
#/////////////////////////////////////////////////////////////
tpc_pedestal_mean = list(itertools.chain.from_iterable(v1740_pedestal_mean[:7]))
tpc_pedestal_mean.extend(v1740_pedestal_mean[7][:32])

tpc_pedestal_rms = list(itertools.chain.from_iterable(v1740_pedestal_rms[:7]))
tpc_pedestal_rms.extend(v1740_pedestal_rms[7][:32])

tpc_adc_mean = list(itertools.chain.from_iterable(v1740_adc_mean[:7]))
tpc_adc_mean.extend(v1740_adc_mean[7][:32])

tpc_adc_rms = list(itertools.chain.from_iterable(v1740_adc_rms[:7]))
tpc_adc_rms.extend(v1740_adc_rms[7][:32])

#/////////////////////////////////////////////////////////////
# get CAEN V1751 ADC histograms
#/////////////////////////////////////////////////////////////
caen_board_8_adc_histograms = {}
caen_board_9_adc_histograms = {}

for channel in v1751_channels:
    # CAEN board 8
    caen_board_8_pedestal_bins, caen_board_8_pedestal_counts = th1_to_arrays(
        f.Get("DataQuality/pedestal/caen_board_8_channel_{}_pedestal"
              .format(channel)))

    caen_board_8_adc_bins, caen_board_8_adc_counts = th1_to_arrays(
        f.Get("DataQuality/adc/caen_board_8_channel_{}_adc".format(channel)))

    caen_board_8_adc_counts += caen_board_8_pedestal_counts  # add pedestal

    caen_board_8_adc_histograms[channel] = Histogram(
        "caen_board_8_channel_{}_adc".format(channel))
    caen_board_8_adc_histograms[channel].histogram_to_db(
        caen_board_8_adc_bins, caen_board_8_adc_counts)

    # CAEN board 9
    caen_board_9_pedestal_bins, caen_board_9_pedestal_counts = th1_to_arrays(
        f.Get("DataQuality/pedestal/caen_board_9_channel_{}_pedestal"
              .format(channel)))

    caen_board_9_adc_bins, caen_board_9_adc_counts = th1_to_arrays(
        f.Get("DataQuality/adc/caen_board_9_channel_{}_adc".format(channel)))

    caen_board_9_adc_counts += caen_board_9_pedestal_counts  # add pedestal

    caen_board_9_adc_histograms[channel] = Histogram(
        "caen_board_9_channel_{}_adc".format(channel))
    caen_board_9_adc_histograms[channel].histogram_to_db(
        caen_board_9_adc_bins, caen_board_9_adc_counts)

#/////////////////////////////////////////////////////////////
# get USTOF hits histogram
#/////////////////////////////////////////////////////////////
ustof_hits_th1 = f.Get(ustof_hits_th1_name)
ustof_hits_bins, ustof_hits_counts = th1_to_arrays(ustof_hits_th1)
ustof_hits_histogram = Histogram("ustof_hits")
ustof_hits_histogram.histogram_to_db(ustof_hits_bins, ustof_hits_counts)

#/////////////////////////////////////////////////////////////
# get DSTOF hits histogram
#/////////////////////////////////////////////////////////////
dstof_hits_th1 = f.Get(dstof_hits_th1_name)
dstof_hits_bins, dstof_hits_counts = th1_to_arrays(dstof_hits_th1)
dstof_hits_histogram = Histogram("dstof_hits")
dstof_hits_histogram.histogram_to_db(dstof_hits_bins, dstof_hits_counts)

#/////////////////////////////////////////////////////////////
# get TOF histogram
#/////////////////////////////////////////////////////////////
tof_th1 = f.Get(tof_th1_name)
tof_bins, tof_counts = th1_to_arrays(tof_th1)
tof_histogram = Histogram("tof")
tof_histogram.histogram_to_db(tof_bins, tof_counts)

#/////////////////////////////////////////////////////////////
# convert time stamp to date time
#/////////////////////////////////////////////////////////////
date_time = datetime.fromtimestamp(timestamp)

#/////////////////////////////////////////////////////////////
# instantiate DataQualitySubRun
#/////////////////////////////////////////////////////////////
SubRun = DataQualitySubRun(
    run=run, subrun=subrun, date_time=date_time,
    date_time_added=datetime.now())

#/////////////////////////////////////////////////////////////
# add number of data blocks to SubRum
#/////////////////////////////////////////////////////////////
for board in caen_boards:
    setattr(SubRun, "caen_board_{}_data_blocks".format(board),
            number_caen_data_blocks[board])
SubRun.mwpc_data_blocks = number_tdc_data_blocks
SubRun.wut_data_blocks = number_wut_data_blocks

#/////////////////////////////////////////////////////////////
# add TPC pedestal/ADC mean and RMS to SubRun
#/////////////////////////////////////////////////////////////
SubRun.tpc_pedestal_mean = tpc_pedestal_mean
SubRun.tpc_pedestal_rms = tpc_pedestal_rms
SubRun.tpc_adc_mean = tpc_adc_mean
SubRun.tpc_adc_rms = tpc_adc_rms

#/////////////////////////////////////////////////////////////
# add CAEN pedestal/ADC mean and RMS to SubRun
#/////////////////////////////////////////////////////////////
SubRun.caen_board_7_pedestal_mean = v1740_pedestal_mean[7][32:]
SubRun.caen_board_7_pedestal_rms = v1740_pedestal_rms[7][32:]
SubRun.caen_board_7_adc_mean = v1740_adc_mean[7][32:]
SubRun.caen_board_7_adc_rms = v1740_adc_rms[7][32:]

for i in xrange(len(v1751_boards)):
    board = v1751_boards[i]
    setattr(SubRun, "caen_board_{}_pedestal_mean".format(board),
            v1751_pedestal_mean[i])
    setattr(SubRun, "caen_board_{}_pedestal_rms".format(board),
            v1751_pedestal_rms[i])
    setattr(SubRun, "caen_board_{}_adc_mean".format(board),
            v1751_adc_mean[i])
    setattr(SubRun, "caen_board_{}_adc_rms".format(board),
            v1751_adc_rms[i])

for i in xrange(len(v1740b_boards)):
    board = v1740b_boards[i]
    setattr(SubRun, "caen_board_{}_pedestal_mean".format(board),
            v1740b_pedestal_mean[i])
    setattr(SubRun, "caen_board_{}_pedestal_rms".format(board),
            v1740b_pedestal_rms[i])
    setattr(SubRun, "caen_board_{}_adc_mean".format(board),
            v1740b_adc_mean[i])
    setattr(SubRun, "caen_board_{}_adc_rms".format(board),
            v1740b_adc_rms[i])

#/////////////////////////////////////////////////////////////
# add CAEN V1751 ADC histograms to SubRun
#/////////////////////////////////////////////////////////////
for channel in v1751_channels:
    # CAEN board 8
    setattr(SubRun,
        "caen_board_8_channel_{}_adc_histogram_bins".format(channel),
        caen_board_8_adc_histograms[channel].bins_sparse)
    setattr(SubRun,
        "caen_board_8_channel_{}_adc_histogram_counts".format(channel),
        caen_board_8_adc_histograms[channel].counts_sparse)

    # CAEN board 9
    setattr(SubRun,
        "caen_board_9_channel_{}_adc_histogram_bins".format(channel),
        caen_board_9_adc_histograms[channel].bins_sparse)
    setattr(SubRun,
        "caen_board_9_channel_{}_adc_histogram_counts".format(channel),
        caen_board_9_adc_histograms[channel].counts_sparse)

#/////////////////////////////////////////////////////////////
# add USTOF hits histogram to SubRun
#/////////////////////////////////////////////////////////////
SubRun.ustof_hits_histogram_bins = ustof_hits_histogram.bins_sparse
SubRun.ustof_hits_histogram_counts = ustof_hits_histogram.counts_sparse
SubRun.ustof_hits_histogram_min_bin = ustof_hits_histogram.min_bin
SubRun.ustof_hits_histogram_max_bin = ustof_hits_histogram.max_bin
SubRun.ustof_hits_histogram_bin_width = ustof_hits_histogram.bin_width

#/////////////////////////////////////////////////////////////
# add DSTOF hits histogram to SubRun
#/////////////////////////////////////////////////////////////
SubRun.dstof_hits_histogram_bins = dstof_hits_histogram.bins_sparse
SubRun.dstof_hits_histogram_counts = dstof_hits_histogram.counts_sparse
SubRun.dstof_hits_histogram_min_bin = dstof_hits_histogram.min_bin
SubRun.dstof_hits_histogram_max_bin = dstof_hits_histogram.max_bin
SubRun.dstof_hits_histogram_bin_width = dstof_hits_histogram.bin_width

#/////////////////////////////////////////////////////////////
# add TOF histogram to SubRun
#/////////////////////////////////////////////////////////////
SubRun.tof_histogram_bins = tof_histogram.bins_sparse
SubRun.tof_histogram_counts = tof_histogram.counts_sparse
SubRun.tof_histogram_min_bin = tof_histogram.min_bin
SubRun.tof_histogram_max_bin = tof_histogram.max_bin
SubRun.tof_histogram_bin_width = tof_histogram.bin_width

# TODO: Add MWPC hits with DBSCAN filtering.

#/////////////////////////////////////////////////////////////
# if run does not exist in database, create it
#/////////////////////////////////////////////////////////////
if not run_exists:

    # instantiate DataQualityRun
    Run = DataQualityRun(
        run=run, date_time=date_time, date_time_added=datetime.now())

    # use existing data in the current SubRun
    subrun_dict = dict(SubRun.__dict__)  # copy SubRun dictionary to new dictionary
    subrun_dict.pop('_sa_instance_state', None)  # remove SubRun state object
    subrun_dict.pop('run', None)  # this is already in Run
    subrun_dict.pop('subrun', None)  # there is a subruns list in Run
    subrun_dict.pop('date_time', None)  # don't mess with datetime
    subrun_dict.pop('date_time_added', None)  # don't mess with datetime
    subrun_dict.pop('date_time_updated', None)  # don't mess with datetime

    # add existing data from current SubRun to Run
    Run.__dict__.update(subrun_dict)

    # add current subrun number to list
    Run.subruns = [ subrun ]

#/////////////////////////////////////////////////////////////
# if run exists in database, update it
#/////////////////////////////////////////////////////////////
elif run_exists:
    result = DataQualityRun.query.filter_by(run=run)

#/////////////////////////////////////////////////////////////
# add SubRun to session
#/////////////////////////////////////////////////////////////
db_session.add(SubRun)
db_session.add(Run)

#/////////////////////////////////////////////////////////////
# attempt to commit changes and additions to database
#/////////////////////////////////////////////////////////////
try:
    db_session.commit()
except IntegrityError as e:
    db_session.rollback()
    print str(e)
except SQLAlchemyError as e:
    db_session.rollback()
    print str(e)

db_session.remove()

print hp.heap()

