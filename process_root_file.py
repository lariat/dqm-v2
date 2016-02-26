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
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

import ROOT
#import root_numpy as rnp

from guppy import hpy

import log
from classes import Histogram

from dqm.database import db_session
from dqm.models import DataQualityRun, DataQualitySubRun, DataQualityLatest
import dqm.allowed as allowed

import mwpc

#/////////////////////////////////////////////////////////////
# heapy
#/////////////////////////////////////////////////////////////
hp = hpy()

#/////////////////////////////////////////////////////////////
# argparse
#/////////////////////////////////////////////////////////////
parser = argparse.ArgumentParser(description="Analyze from ROOT file.")
parser.add_argument('file', type=str, help="path to ROOT file")
parser.add_argument('--backlog', dest='backlog', action='store_true',
    help="backlog mode, prevents updating the DataQualityLatest table")
args = parser.parse_args()

#/////////////////////////////////////////////////////////////
# iterators for CAEN boards and channels
#/////////////////////////////////////////////////////////////
v1740_boards = allowed.v1740_boards
v1751_boards = allowed.v1751_boards
v1740b_boards = allowed.v1740b_boards
caen_boards = allowed.caen_boards
non_tpc_caen_boards = allowed.non_tpc_caen_boards

v1740_channels = allowed.v1740_channels
v1751_channels = allowed.v1751_channels
v1740b_channels = allowed.v1740b_channels

#/////////////////////////////////////////////////////////////
# iterators for MWC TDCs
#/////////////////////////////////////////////////////////////
mwc_tdc_numbers = allowed.mwc_tdc_numbers
mwc_tdc_channels = allowed.mwc_tdc_channels
mwc_tdc_clock_ticks = allowed.mwc_tdc_clock_ticks

#/////////////////////////////////////////////////////////////
# histogram names
#/////////////////////////////////////////////////////////////
pedestal_th1_name = "DataQuality/pedestal/caen_board_{}_channel_{}_pedestal"
adc_th1_name = "DataQuality/adc/caen_board_{}_channel_{}_adc"
caen_timestamps_th1_name = "DataQuality/timestamps/caen_board_{}_timestamps"
mwc_tdc_timestamps_th1_name = "DataQuality/timestamps/mwpc_tdc_timestamps"
wut_timestamps_th1_name = "DataQuality/timestamps/wut_timestamps"
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
timestamps_bins = 120

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
    number_bins = th1.GetSize()
    for bin_index in xrange(number_bins):
        if th1.IsBinUnderflow(bin_index) or th1.IsBinOverflow(bin_index):
            continue
        bins.append(th1.GetBinLowEdge(bin_index))
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

# loop over EventBuilder TTree
for branch in event_builder_ttree:
    number_events += 1
    number_tpc_events += branch.NumberTPCReadouts

    for board in caen_boards:
        number_caen_data_blocks[board] += getattr(
            branch, "NumberCAENBoard{}Blocks".format(board))

    number_tdc_data_blocks += branch.NumberTDCBlocks

# loop over WUT TTree
for branch in wut_ttree:
    number_wut_data_blocks += 1

#/////////////////////////////////////////////////////////////
# get histograms for timestamps of data blocks
#/////////////////////////////////////////////////////////////
caen_timestamps_counts = { board : [] for board in caen_boards }
caen_timestamps_bins = { board : [] for board in caen_boards }
caen_timestamps_histograms = {
    board : Histogram("caen_board_{}_timestamps".format(board))
    for board in caen_boards }

for board in caen_boards:
    # get histogram for CAEN timestamps
    caen_timestamps_bins[board], caen_timestamps_counts[board] = th1_to_arrays(
        f.Get(caen_timestamps_th1_name.format(board)))

    # use Histogram class for CAEN timestamps
    caen_timestamps_histograms[board].histogram_to_db(
        caen_timestamps_bins[board], caen_timestamps_counts[board])

#/////////////////////////////////////////////////////////////
# get MWC TDC timestamps
#/////////////////////////////////////////////////////////////
mwc_tdc_timestamps_th1 = f.Get(mwc_tdc_timestamps_th1_name)
mwc_tdc_timestamps_bins, mwc_tdc_timestamps_counts = th1_to_arrays(
    mwc_tdc_timestamps_th1)
mwc_tdc_timestamps_histogram = Histogram("mwc_tdc_timestamps")
mwc_tdc_timestamps_histogram.histogram_to_db(
    mwc_tdc_timestamps_bins, mwc_tdc_timestamps_counts)

#/////////////////////////////////////////////////////////////
# get WUT timestamps
#/////////////////////////////////////////////////////////////
wut_timestamps_th1 = f.Get(wut_timestamps_th1_name)
wut_timestamps_bins, wut_timestamps_counts = th1_to_arrays(wut_timestamps_th1)
wut_timestamps_histogram = Histogram("wut_timestamps")
wut_timestamps_histogram.histogram_to_db(
    wut_timestamps_bins, wut_timestamps_counts)

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
# get MWC histograms
#/////////////////////////////////////////////////////////////
mwc_ok = False

try:
    good_hits, bad_hits = mwpc.get_hits(args.file)
    mwc_ok = True
except:
    mwc_ok =False

if mwc_ok:
    mwc_good_hits_channel_histograms = mwpc.hits_histograms(
        good_hits, 0, mwc_tdc_numbers, mwc_tdc_channels)
    mwc_bad_hits_channel_histograms = mwpc.hits_histograms(
        bad_hits, 0, mwc_tdc_numbers, mwc_tdc_channels)
    mwc_good_hits_timing_histograms = mwpc.hits_histograms(
        good_hits, 1, mwc_tdc_numbers, mwc_tdc_clock_ticks)
    mwc_bad_hits_timing_histograms = mwpc.hits_histograms(
        bad_hits, 1, mwc_tdc_numbers, mwc_tdc_clock_ticks)

#/////////////////////////////////////////////////////////////
# convert time stamp to date time
#/////////////////////////////////////////////////////////////
date_time = datetime.fromtimestamp(timestamp)

#------------------------------------------------------------------------------
# ADD TO dqm.subruns TABLE
#------------------------------------------------------------------------------

#/////////////////////////////////////////////////////////////
# instantiate DataQualitySubRun
#/////////////////////////////////////////////////////////////
SubRun = DataQualitySubRun(
    run=run, subrun=subrun, date_time=date_time,
    date_time_added=datetime.now())

#/////////////////////////////////////////////////////////////
# add number of events to SubRun
#/////////////////////////////////////////////////////////////
SubRun.number_events = number_events
SubRun.number_tpc_events = number_tpc_events

#/////////////////////////////////////////////////////////////
# add number of data blocks to SubRun
#/////////////////////////////////////////////////////////////
for board in caen_boards:
    setattr(SubRun, "caen_board_{}_data_blocks".format(board),
            number_caen_data_blocks[board])
SubRun.mwc_data_blocks = number_tdc_data_blocks
SubRun.wut_data_blocks = number_wut_data_blocks

#/////////////////////////////////////////////////////////////
# add histograms of data block timestamps to SubRun
#/////////////////////////////////////////////////////////////
for board in caen_boards:
    setattr(SubRun,
        "caen_board_{}_timestamps_histogram_bins".format(board),
        caen_timestamps_histograms[board].bins_sparse)
    setattr(SubRun,
        "caen_board_{}_timestamps_histogram_counts".format(board),
        caen_timestamps_histograms[board].counts_sparse)
    setattr(SubRun,
        "caen_board_{}_timestamps_histogram_min_bin".format(board),
        caen_timestamps_histograms[board].min_bin)
    setattr(SubRun,
        "caen_board_{}_timestamps_histogram_max_bin".format(board),
        caen_timestamps_histograms[board].max_bin)
    setattr(SubRun,
        "caen_board_{}_timestamps_histogram_bin_width".format(board),
        caen_timestamps_histograms[board].bin_width)

SubRun.mwc_tdc_timestamps_histogram_bins = mwc_tdc_timestamps_histogram.bins_sparse
SubRun.mwc_tdc_timestamps_histogram_counts = mwc_tdc_timestamps_histogram.counts_sparse
SubRun.mwc_tdc_timestamps_histogram_min_bin = mwc_tdc_timestamps_histogram.min_bin
SubRun.mwc_tdc_timestamps_histogram_max_bin = mwc_tdc_timestamps_histogram.max_bin
SubRun.mwc_tdc_timestamps_histogram_bin_width = mwc_tdc_timestamps_histogram.bin_width

SubRun.wut_timestamps_histogram_bins = wut_timestamps_histogram.bins_sparse
SubRun.wut_timestamps_histogram_counts = wut_timestamps_histogram.counts_sparse
SubRun.wut_timestamps_histogram_min_bin = wut_timestamps_histogram.min_bin
SubRun.wut_timestamps_histogram_max_bin = wut_timestamps_histogram.max_bin
SubRun.wut_timestamps_histogram_bin_width = wut_timestamps_histogram.bin_width

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
    setattr(SubRun,
        "caen_board_8_channel_{}_adc_histogram_min_bin".format(channel),
        caen_board_8_adc_histograms[channel].min_bin)
    setattr(SubRun,
        "caen_board_8_channel_{}_adc_histogram_max_bin".format(channel),
        caen_board_8_adc_histograms[channel].max_bin)
    setattr(SubRun,
        "caen_board_8_channel_{}_adc_histogram_bin_width".format(channel),
        caen_board_8_adc_histograms[channel].bin_width)

    # CAEN board 9
    setattr(SubRun,
        "caen_board_9_channel_{}_adc_histogram_bins".format(channel),
        caen_board_9_adc_histograms[channel].bins_sparse)
    setattr(SubRun,
        "caen_board_9_channel_{}_adc_histogram_counts".format(channel),
        caen_board_9_adc_histograms[channel].counts_sparse)
    setattr(SubRun,
        "caen_board_9_channel_{}_adc_histogram_min_bin".format(channel),
        caen_board_9_adc_histograms[channel].min_bin)
    setattr(SubRun,
        "caen_board_9_channel_{}_adc_histogram_max_bin".format(channel),
        caen_board_9_adc_histograms[channel].max_bin)
    setattr(SubRun,
        "caen_board_9_channel_{}_adc_histogram_bin_width".format(channel),
        caen_board_9_adc_histograms[channel].bin_width)

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

#/////////////////////////////////////////////////////////////
# add MWC TDC hits histograms to SubRun
#/////////////////////////////////////////////////////////////
if mwc_ok:
    for tdc in mwc_tdc_numbers:
        # channel occupancy for good hits
        setattr(SubRun,
            "mwc_tdc_{}_good_hits_channel_histogram_bins".format(tdc),
            mwc_good_hits_channel_histograms[tdc].bins_sparse)
        setattr(SubRun,
            "mwc_tdc_{}_good_hits_channel_histogram_counts".format(tdc),
            mwc_good_hits_channel_histograms[tdc].counts_sparse)
        setattr(SubRun,
            "mwc_tdc_{}_good_hits_channel_histogram_min_bin".format(tdc),
            mwc_good_hits_channel_histograms[tdc].min_bin)
        setattr(SubRun,
            "mwc_tdc_{}_good_hits_channel_histogram_max_bin".format(tdc),
            mwc_good_hits_channel_histograms[tdc].max_bin)
        setattr(SubRun,
            "mwc_tdc_{}_good_hits_channel_histogram_bin_width".format(tdc),
            mwc_good_hits_channel_histograms[tdc].bin_width)

        # channel occupancy for bad hits
        setattr(SubRun,
            "mwc_tdc_{}_bad_hits_channel_histogram_bins".format(tdc),
            mwc_bad_hits_channel_histograms[tdc].bins_sparse)
        setattr(SubRun,
            "mwc_tdc_{}_bad_hits_channel_histogram_counts".format(tdc),
            mwc_bad_hits_channel_histograms[tdc].counts_sparse)
        setattr(SubRun,
            "mwc_tdc_{}_bad_hits_channel_histogram_min_bin".format(tdc),
            mwc_bad_hits_channel_histograms[tdc].min_bin)
        setattr(SubRun,
            "mwc_tdc_{}_bad_hits_channel_histogram_max_bin".format(tdc),
            mwc_bad_hits_channel_histograms[tdc].max_bin)
        setattr(SubRun,
            "mwc_tdc_{}_bad_hits_channel_histogram_bin_width".format(tdc),
            mwc_bad_hits_channel_histograms[tdc].bin_width)

        # timing occupancy for good hits
        setattr(SubRun,
            "mwc_tdc_{}_good_hits_timing_histogram_bins".format(tdc),
            mwc_good_hits_timing_histograms[tdc].bins_sparse)
        setattr(SubRun,
            "mwc_tdc_{}_good_hits_timing_histogram_counts".format(tdc),
            mwc_good_hits_timing_histograms[tdc].counts_sparse)
        setattr(SubRun,
            "mwc_tdc_{}_good_hits_timing_histogram_min_bin".format(tdc),
            mwc_good_hits_timing_histograms[tdc].min_bin)
        setattr(SubRun,
            "mwc_tdc_{}_good_hits_timing_histogram_max_bin".format(tdc),
            mwc_good_hits_timing_histograms[tdc].max_bin)
        setattr(SubRun,
            "mwc_tdc_{}_good_hits_timing_histogram_bin_width".format(tdc),
            mwc_good_hits_timing_histograms[tdc].bin_width)

        # timing occupancy for bad hits
        setattr(SubRun,
            "mwc_tdc_{}_bad_hits_timing_histogram_bins".format(tdc),
            mwc_bad_hits_timing_histograms[tdc].bins_sparse)
        setattr(SubRun,
            "mwc_tdc_{}_bad_hits_timing_histogram_counts".format(tdc),
            mwc_bad_hits_timing_histograms[tdc].counts_sparse)
        setattr(SubRun,
            "mwc_tdc_{}_bad_hits_timing_histogram_min_bin".format(tdc),
            mwc_bad_hits_timing_histograms[tdc].min_bin)
        setattr(SubRun,
            "mwc_tdc_{}_bad_hits_timing_histogram_max_bin".format(tdc),
            mwc_bad_hits_timing_histograms[tdc].max_bin)
        setattr(SubRun,
            "mwc_tdc_{}_bad_hits_timing_histogram_bin_width".format(tdc),
            mwc_bad_hits_timing_histograms[tdc].bin_width)

#------------------------------------------------------------------------------
# ADD TO dqm.runs TABLE
#------------------------------------------------------------------------------

# add run to database only if this is true
run_ok = False

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

    # OK to add run to database
    run_ok = True

#/////////////////////////////////////////////////////////////
# if run exists in database, update it
#/////////////////////////////////////////////////////////////
elif run_exists:

    try:
        Run = DataQualityRun.query.filter_by(run=run).one()

        #/////////////////////////////////////////////////////
        # add pedestal/ADC mean and RMS of TPC wires/channels
        # to Run from SubRun; we want the most recent values
        #/////////////////////////////////////////////////////
        Run.tpc_pedestal_mean = SubRun.tpc_pedestal_mean
        Run.tpc_pedestal_rms = SubRun.tpc_pedestal_rms
        Run.tpc_adc_mean = SubRun.tpc_adc_mean
        Run.tpc_adc_rms = SubRun.tpc_adc_rms

        #/////////////////////////////////////////////////////
        # add pedestal/ADC mean and RMS of CAEN boards to Run
        # from SubRun; we want the most recent values
        #/////////////////////////////////////////////////////
        Run.caen_board_7_pedestal_mean = SubRun.caen_board_7_pedestal_mean
        Run.caen_board_8_pedestal_mean = SubRun.caen_board_8_pedestal_mean
        Run.caen_board_9_pedestal_mean = SubRun.caen_board_9_pedestal_mean
        Run.caen_board_24_pedestal_mean = SubRun.caen_board_24_pedestal_mean

        Run.caen_board_7_pedestal_rms = SubRun.caen_board_7_pedestal_rms
        Run.caen_board_8_pedestal_rms = SubRun.caen_board_8_pedestal_rms
        Run.caen_board_9_pedestal_rms = SubRun.caen_board_9_pedestal_rms
        Run.caen_board_24_pedestal_rms = SubRun.caen_board_24_pedestal_rms

        Run.caen_board_7_adc_mean = SubRun.caen_board_7_adc_mean
        Run.caen_board_8_adc_mean = SubRun.caen_board_8_adc_mean
        Run.caen_board_9_adc_mean = SubRun.caen_board_9_adc_mean
        Run.caen_board_24_adc_mean = SubRun.caen_board_24_adc_mean

        Run.caen_board_7_adc_rms = SubRun.caen_board_7_adc_rms
        Run.caen_board_8_adc_rms = SubRun.caen_board_8_adc_rms
        Run.caen_board_9_adc_rms = SubRun.caen_board_9_adc_rms
        Run.caen_board_24_adc_rms = SubRun.caen_board_24_adc_rms

        #/////////////////////////////////////////////////////////////
        # update number of events in Run
        #/////////////////////////////////////////////////////////////
        Run.number_events += number_events
        Run.number_tpc_events += number_tpc_events

        #/////////////////////////////////////////////////////////////
        # update number of data blocks in Run
        #/////////////////////////////////////////////////////////////
        for board in caen_boards:
            attribute = "caen_board_{}_data_blocks".format(board)
            setattr(Run, attribute, getattr(Run, attribute) + \
                    number_caen_data_blocks[board])
        Run.mwc_data_blocks += number_tdc_data_blocks
        Run.wut_data_blocks += number_wut_data_blocks

        #/////////////////////////////////////////////////////////////
        # update histograms of data block timestamps in Run
        #/////////////////////////////////////////////////////////////
        # CAEN timestamps
        run_caen_timestamps_histograms = {}

        for board in caen_boards:
            run_caen_timestamps_histograms[board] = Histogram(
                "caen_board_{}_timestamps".format(board))

            run_caen_timestamps_histograms[board].db_to_histogram(
                getattr(Run, "caen_board_{}_timestamps_histogram_bins".format(board)),
                getattr(Run, "caen_board_{}_timestamps_histogram_counts".format(board)),
                getattr(Run, "caen_board_{}_timestamps_histogram_min_bin".format(board)),
                getattr(Run, "caen_board_{}_timestamps_histogram_max_bin".format(board)),
                getattr(Run, "caen_board_{}_timestamps_histogram_bin_width".format(board)))

            run_caen_timestamps_histograms[board] += caen_timestamps_histograms[board]

            setattr(Run,
                "caen_board_{}_timestamps_histogram_bins".format(board),
                run_caen_timestamps_histograms[board].bins_sparse)
            setattr(Run,
                "caen_board_{}_timestamps_histogram_counts".format(board),
                run_caen_timestamps_histograms[board].counts_sparse)
            setattr(Run,
                "caen_board_{}_timestamps_histogram_min_bin".format(board),
                run_caen_timestamps_histograms[board].min_bin)
            setattr(Run,
                "caen_board_{}_timestamps_histogram_max_bin".format(board),
                run_caen_timestamps_histograms[board].max_bin)
            setattr(Run,
                "caen_board_{}_timestamps_histogram_bin_width".format(board),
                run_caen_timestamps_histograms[board].bin_width)

        # MWC TDC timestamps
        run_mwc_tdc_timestamps_histogram = Histogram("run_mwc_tdc_timestamps")

        run_mwc_tdc_timestamps_histogram.db_to_histogram(
            Run.mwc_tdc_timestamps_histogram_bins,
            Run.mwc_tdc_timestamps_histogram_counts,
            Run.mwc_tdc_timestamps_histogram_min_bin,
            Run.mwc_tdc_timestamps_histogram_max_bin,
            Run.mwc_tdc_timestamps_histogram_bin_width)

        run_mwc_tdc_timestamps_histogram += mwc_tdc_timestamps_histogram

        Run.mwc_tdc_timestamps_histogram_bins = run_mwc_tdc_timestamps_histogram.bins_sparse
        Run.mwc_tdc_timestamps_histogram_counts = run_mwc_tdc_timestamps_histogram.counts_sparse
        Run.mwc_tdc_timestamps_histogram_min_bin = run_mwc_tdc_timestamps_histogram.min_bin
        Run.mwc_tdc_timestamps_histogram_max_bin = run_mwc_tdc_timestamps_histogram.max_bin
        Run.mwc_tdc_timestamps_histogram_bin_width = run_mwc_tdc_timestamps_histogram.bin_width

        # WUT timestamps
        run_wut_timestamps_histogram = Histogram("run_wut_timestamps")

        run_wut_timestamps_histogram.db_to_histogram(
            Run.wut_timestamps_histogram_bins,
            Run.wut_timestamps_histogram_counts,
            Run.wut_timestamps_histogram_min_bin,
            Run.wut_timestamps_histogram_max_bin,
            Run.wut_timestamps_histogram_bin_width)

        run_wut_timestamps_histogram += wut_timestamps_histogram

        Run.wut_timestamps_histogram_bins = run_wut_timestamps_histogram.bins_sparse
        Run.wut_timestamps_histogram_counts = run_wut_timestamps_histogram.counts_sparse
        Run.wut_timestamps_histogram_min_bin = run_wut_timestamps_histogram.min_bin
        Run.wut_timestamps_histogram_max_bin = run_wut_timestamps_histogram.max_bin
        Run.wut_timestamps_histogram_bin_width = run_wut_timestamps_histogram.bin_width

        #/////////////////////////////////////////////////////
        # update CAEN V1751 ADC histograms to Run
        #/////////////////////////////////////////////////////
        run_caen_board_8_adc_histograms = {}
        run_caen_board_9_adc_histograms = {}

        for channel in v1751_channels:
            # CAEN board 8
            run_caen_board_8_adc_histograms[channel] = Histogram(
                "caen_board_8_channel_{}_adc".format(channel))

            run_caen_board_8_adc_histograms[channel].db_to_histogram(
                getattr(Run, "caen_board_8_channel_{}_adc_histogram_bins".format(channel)),
                getattr(Run, "caen_board_8_channel_{}_adc_histogram_counts".format(channel)),
                getattr(Run, "caen_board_8_channel_{}_adc_histogram_min_bin".format(channel)),
                getattr(Run, "caen_board_8_channel_{}_adc_histogram_max_bin".format(channel)),
                getattr(Run, "caen_board_8_channel_{}_adc_histogram_bin_width".format(channel)))

            run_caen_board_8_adc_histograms[channel] += caen_board_8_adc_histograms[channel]

            setattr(Run,
                "caen_board_8_channel_{}_adc_histogram_bins".format(channel),
                run_caen_board_8_adc_histograms[channel].bins_sparse)
            setattr(Run,
                "caen_board_8_channel_{}_adc_histogram_counts".format(channel),
                run_caen_board_8_adc_histograms[channel].counts_sparse)
            setattr(Run,
                "caen_board_8_channel_{}_adc_histogram_min_bin".format(channel),
                run_caen_board_8_adc_histograms[channel].min_bin)
            setattr(Run,
                "caen_board_8_channel_{}_adc_histogram_max_bin".format(channel),
                run_caen_board_8_adc_histograms[channel].max_bin)
            setattr(Run,
                "caen_board_8_channel_{}_adc_histogram_bin_width".format(channel),
                run_caen_board_8_adc_histograms[channel].bin_width)

            # CAEN board 9
            run_caen_board_9_adc_histograms[channel] = Histogram(
                "caen_board_9_channel_{}_adc".format(channel))

            run_caen_board_9_adc_histograms[channel].db_to_histogram(
                getattr(Run, "caen_board_9_channel_{}_adc_histogram_bins".format(channel)),
                getattr(Run, "caen_board_9_channel_{}_adc_histogram_counts".format(channel)),
                getattr(Run, "caen_board_9_channel_{}_adc_histogram_min_bin".format(channel)),
                getattr(Run, "caen_board_9_channel_{}_adc_histogram_max_bin".format(channel)),
                getattr(Run, "caen_board_9_channel_{}_adc_histogram_bin_width".format(channel)))

            run_caen_board_9_adc_histograms[channel] += caen_board_9_adc_histograms[channel]

            setattr(Run,
                "caen_board_9_channel_{}_adc_histogram_bins".format(channel),
                run_caen_board_9_adc_histograms[channel].bins_sparse)
            setattr(Run,
                "caen_board_9_channel_{}_adc_histogram_counts".format(channel),
                run_caen_board_9_adc_histograms[channel].counts_sparse)
            setattr(Run,
                "caen_board_9_channel_{}_adc_histogram_min_bin".format(channel),
                run_caen_board_9_adc_histograms[channel].min_bin)
            setattr(Run,
                "caen_board_9_channel_{}_adc_histogram_max_bin".format(channel),
                run_caen_board_9_adc_histograms[channel].max_bin)
            setattr(Run,
                "caen_board_9_channel_{}_adc_histogram_bin_width".format(channel),
                run_caen_board_9_adc_histograms[channel].bin_width)

        #/////////////////////////////////////////////////////
        # update USTOF hits histogram in Run
        #/////////////////////////////////////////////////////
        run_ustof_hits_histogram = Histogram("run_ustof_hits")

        run_ustof_hits_histogram.db_to_histogram(
            Run.ustof_hits_histogram_bins,
            Run.ustof_hits_histogram_counts,
            Run.ustof_hits_histogram_min_bin,
            Run.ustof_hits_histogram_max_bin,
            Run.ustof_hits_histogram_bin_width)

        run_ustof_hits_histogram += ustof_hits_histogram

        Run.ustof_hits_histogram_bins = run_ustof_hits_histogram.bins_sparse
        Run.ustof_hits_histogram_counts = run_ustof_hits_histogram.counts_sparse
        Run.ustof_hits_histogram_min_bin = run_ustof_hits_histogram.min_bin
        Run.ustof_hits_histogram_max_bin = run_ustof_hits_histogram.max_bin
        Run.ustof_hits_histogram_bin_width = run_ustof_hits_histogram.bin_width

        #/////////////////////////////////////////////////////
        # update DSTOF hits histogram in Run
        #/////////////////////////////////////////////////////
        run_dstof_hits_histogram = Histogram("run_dstof_hits")

        run_dstof_hits_histogram.db_to_histogram(
            Run.dstof_hits_histogram_bins,
            Run.dstof_hits_histogram_counts,
            Run.dstof_hits_histogram_min_bin,
            Run.dstof_hits_histogram_max_bin,
            Run.dstof_hits_histogram_bin_width)

        run_dstof_hits_histogram += dstof_hits_histogram

        Run.dstof_hits_histogram_bins = run_dstof_hits_histogram.bins_sparse
        Run.dstof_hits_histogram_counts = run_dstof_hits_histogram.counts_sparse
        Run.dstof_hits_histogram_min_bin = run_dstof_hits_histogram.min_bin
        Run.dstof_hits_histogram_max_bin = run_dstof_hits_histogram.max_bin
        Run.dstof_hits_histogram_bin_width = run_dstof_hits_histogram.bin_width

        #/////////////////////////////////////////////////////
        # update TOF histogram in Run
        #/////////////////////////////////////////////////////
        run_tof_histogram = Histogram("run_tof")

        run_tof_histogram.db_to_histogram(Run.tof_histogram_bins,
                                          Run.tof_histogram_counts,
                                          Run.tof_histogram_min_bin,
                                          Run.tof_histogram_max_bin,
                                          Run.tof_histogram_bin_width)

        run_tof_histogram += tof_histogram

        Run.tof_histogram_bins = run_tof_histogram.bins_sparse
        Run.tof_histogram_counts = run_tof_histogram.counts_sparse
        Run.tof_histogram_min_bin = run_tof_histogram.min_bin
        Run.tof_histogram_max_bin = run_tof_histogram.max_bin
        Run.tof_histogram_bin_width = run_tof_histogram.bin_width

        #/////////////////////////////////////////////////////////////
        # update MWC TDC hits histograms in SubRun
        #/////////////////////////////////////////////////////////////
        if mwc_ok:
            run_mwc_good_hits_channel_histograms = {}
            run_mwc_bad_hits_channel_histograms = {}
            run_mwc_good_hits_timing_histograms = {}
            run_mwc_bad_hits_timing_histograms = {}

            for tdc in mwc_tdc_numbers:

                # channel occupancy for good hits
                run_mwc_good_hits_channel_histograms[tdc] = Histogram(
                    "mwc_tdc_{}_good_hits_channel_histogram".format(tdc))

                run_mwc_good_hits_channel_histograms[tdc].db_to_histogram(
                    getattr(Run, "mwc_tdc_{}_good_hits_channel_histogram_bins".format(tdc)),
                    getattr(Run, "mwc_tdc_{}_good_hits_channel_histogram_counts".format(tdc)),
                    getattr(Run, "mwc_tdc_{}_good_hits_channel_histogram_min_bin".format(tdc)),
                    getattr(Run, "mwc_tdc_{}_good_hits_channel_histogram_max_bin".format(tdc)),
                    getattr(Run, "mwc_tdc_{}_good_hits_channel_histogram_bin_width".format(tdc)))

                run_mwc_good_hits_channel_histograms[tdc] += \
                    mwc_good_hits_channel_histograms[tdc]

                setattr(Run,
                    "mwc_tdc_{}_good_hits_channel_histogram_bins".format(tdc),
                    run_mwc_good_hits_channel_histograms[tdc].bins_sparse)
                setattr(Run,
                    "mwc_tdc_{}_good_hits_channel_histogram_counts".format(tdc),
                    run_mwc_good_hits_channel_histograms[tdc].counts_sparse)
                setattr(Run,
                    "mwc_tdc_{}_good_hits_channel_histogram_min_bin".format(tdc),
                    run_mwc_good_hits_channel_histograms[tdc].min_bin)
                setattr(Run,
                    "mwc_tdc_{}_good_hits_channel_histogram_max_bin".format(tdc),
                    run_mwc_good_hits_channel_histograms[tdc].max_bin)
                setattr(Run,
                    "mwc_tdc_{}_good_hits_channel_histogram_bin_width".format(tdc),
                    run_mwc_good_hits_channel_histograms[tdc].bin_width)

                # channel occupancy for bad hits
                run_mwc_bad_hits_channel_histograms[tdc] = Histogram(
                    "mwc_tdc_{}_bad_hits_channel_histogram".format(tdc))

                run_mwc_bad_hits_channel_histograms[tdc].db_to_histogram(
                    getattr(Run, "mwc_tdc_{}_bad_hits_channel_histogram_bins".format(tdc)),
                    getattr(Run, "mwc_tdc_{}_bad_hits_channel_histogram_counts".format(tdc)),
                    getattr(Run, "mwc_tdc_{}_bad_hits_channel_histogram_min_bin".format(tdc)),
                    getattr(Run, "mwc_tdc_{}_bad_hits_channel_histogram_max_bin".format(tdc)),
                    getattr(Run, "mwc_tdc_{}_bad_hits_channel_histogram_bin_width".format(tdc)))

                run_mwc_bad_hits_channel_histograms[tdc] += \
                    mwc_bad_hits_channel_histograms[tdc]

                setattr(Run,
                    "mwc_tdc_{}_bad_hits_channel_histogram_bins".format(tdc),
                    run_mwc_bad_hits_channel_histograms[tdc].bins_sparse)
                setattr(Run,
                    "mwc_tdc_{}_bad_hits_channel_histogram_counts".format(tdc),
                    run_mwc_bad_hits_channel_histograms[tdc].counts_sparse)
                setattr(Run,
                    "mwc_tdc_{}_bad_hits_channel_histogram_min_bin".format(tdc),
                    run_mwc_bad_hits_channel_histograms[tdc].min_bin)
                setattr(Run,
                    "mwc_tdc_{}_bad_hits_channel_histogram_max_bin".format(tdc),
                    run_mwc_bad_hits_channel_histograms[tdc].max_bin)
                setattr(Run,
                    "mwc_tdc_{}_bad_hits_channel_histogram_bin_width".format(tdc),
                    run_mwc_bad_hits_channel_histograms[tdc].bin_width)

                # timing occupancy for good hits
                run_mwc_good_hits_timing_histograms[tdc] = Histogram(
                    "mwc_tdc_{}_good_hits_timing_histogram".format(tdc))

                run_mwc_good_hits_timing_histograms[tdc].db_to_histogram(
                    getattr(Run, "mwc_tdc_{}_good_hits_timing_histogram_bins".format(tdc)),
                    getattr(Run, "mwc_tdc_{}_good_hits_timing_histogram_counts".format(tdc)),
                    getattr(Run, "mwc_tdc_{}_good_hits_timing_histogram_min_bin".format(tdc)),
                    getattr(Run, "mwc_tdc_{}_good_hits_timing_histogram_max_bin".format(tdc)),
                    getattr(Run, "mwc_tdc_{}_good_hits_timing_histogram_bin_width".format(tdc)))

                run_mwc_good_hits_timing_histograms[tdc] += \
                    mwc_good_hits_timing_histograms[tdc]

                setattr(Run,
                    "mwc_tdc_{}_good_hits_timing_histogram_bins".format(tdc),
                    run_mwc_good_hits_timing_histograms[tdc].bins_sparse)
                setattr(Run,
                    "mwc_tdc_{}_good_hits_timing_histogram_counts".format(tdc),
                    run_mwc_good_hits_timing_histograms[tdc].counts_sparse)
                setattr(Run,
                    "mwc_tdc_{}_good_hits_timing_histogram_min_bin".format(tdc),
                    run_mwc_good_hits_timing_histograms[tdc].min_bin)
                setattr(Run,
                    "mwc_tdc_{}_good_hits_timing_histogram_max_bin".format(tdc),
                    run_mwc_good_hits_timing_histograms[tdc].max_bin)
                setattr(Run,
                    "mwc_tdc_{}_good_hits_timing_histogram_bin_width".format(tdc),
                    run_mwc_good_hits_timing_histograms[tdc].bin_width)

                # timing occupancy for bad hits
                run_mwc_bad_hits_timing_histograms[tdc] = Histogram(
                    "mwc_tdc_{}_bad_hits_timing_histogram".format(tdc))

                run_mwc_bad_hits_timing_histograms[tdc].db_to_histogram(
                    getattr(Run, "mwc_tdc_{}_bad_hits_timing_histogram_bins".format(tdc)),
                    getattr(Run, "mwc_tdc_{}_bad_hits_timing_histogram_counts".format(tdc)),
                    getattr(Run, "mwc_tdc_{}_bad_hits_timing_histogram_min_bin".format(tdc)),
                    getattr(Run, "mwc_tdc_{}_bad_hits_timing_histogram_max_bin".format(tdc)),
                    getattr(Run, "mwc_tdc_{}_bad_hits_timing_histogram_bin_width".format(tdc)))

                run_mwc_bad_hits_timing_histograms[tdc] += \
                    mwc_bad_hits_timing_histograms[tdc]

                setattr(Run,
                    "mwc_tdc_{}_bad_hits_timing_histogram_bins".format(tdc),
                    run_mwc_bad_hits_timing_histograms[tdc].bins_sparse)
                setattr(Run,
                    "mwc_tdc_{}_bad_hits_timing_histogram_counts".format(tdc),
                    run_mwc_bad_hits_timing_histograms[tdc].counts_sparse)
                setattr(Run,
                    "mwc_tdc_{}_bad_hits_timing_histogram_min_bin".format(tdc),
                    run_mwc_bad_hits_timing_histograms[tdc].min_bin)
                setattr(Run,
                    "mwc_tdc_{}_bad_hits_timing_histogram_max_bin".format(tdc),
                    run_mwc_bad_hits_timing_histograms[tdc].max_bin)
                setattr(Run,
                    "mwc_tdc_{}_bad_hits_timing_histogram_bin_width".format(tdc),
                    run_mwc_bad_hits_timing_histograms[tdc].bin_width)

        #/////////////////////////////////////////////////////
        # update subruns list in Run
        #/////////////////////////////////////////////////////
        run_subruns = list(Run.subruns)
        run_subruns.append(subrun)
        Run.subruns = run_subruns

        #/////////////////////////////////////////////////////
        # update datetime
        #/////////////////////////////////////////////////////
        Run.date_time_updated = datetime.now()

        # OK to add run to database
        run_ok = True

    except MultipleResultsFound as e:
        print str(e)
    except NoResultFound as e:
        print str(e)

#/////////////////////////////////////////////////////////////
# add SubRun to session
#/////////////////////////////////////////////////////////////
db_session.add(SubRun)

#/////////////////////////////////////////////////////////////
# add Run to session
#/////////////////////////////////////////////////////////////
if run_ok:
    db_session.add(Run)

#/////////////////////////////////////////////////////////////
# update Latest with latest run and sub-run
#/////////////////////////////////////////////////////////////
if not args.backlog:
    Latest = DataQualityLatest.query.order_by(
        DataQualityLatest.date_time_updated.desc()).first()
    Latest.run = run
    Latest.subrun = subrun
    Latest.date_time_updated = datetime.now()
    db_session.add(Latest)

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

