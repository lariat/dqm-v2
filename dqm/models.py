from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.dialects.postgresql import ARRAY

from dqm.database import Base

class DataQualityMixin(object):
    """ Data quality mixin. """

    #/////////////////////////////////////////////////////////
    # psql sequence for unique ID
    #/////////////////////////////////////////////////////////
    id = Column(Integer, primary_key=True)

    #/////////////////////////////////////////////////////////
    # date/time
    #/////////////////////////////////////////////////////////
    date_time = Column(
        DateTime(timezone=False), unique=False, nullable=False)
    date_time_added = Column(
        DateTime(timezone=False), unique=False, nullable=False)
    date_time_updated = Column(
        DateTime(timezone=False), unique=False, nullable=False)

    #/////////////////////////////////////////////////////////
    # run number
    #/////////////////////////////////////////////////////////
    run = Column(Integer, unique=False)

    #/////////////////////////////////////////////////////////
    # number of data blocks
    #/////////////////////////////////////////////////////////
    #caen_data_blocks = Column(ARRAY(Integer), unique=False)
    caen_board_0_data_blocks = Column(Integer, unique=False)
    caen_board_1_data_blocks = Column(Integer, unique=False)
    caen_board_2_data_blocks = Column(Integer, unique=False)
    caen_board_3_data_blocks = Column(Integer, unique=False)
    caen_board_4_data_blocks = Column(Integer, unique=False)
    caen_board_5_data_blocks = Column(Integer, unique=False)
    caen_board_6_data_blocks = Column(Integer, unique=False)
    caen_board_7_data_blocks = Column(Integer, unique=False)
    caen_board_8_data_blocks = Column(Integer, unique=False)
    caen_board_9_data_blocks = Column(Integer, unique=False)
    caen_board_24_data_blocks = Column(Integer, unique=False)
    mwpc_data_blocks = Column(Integer, unique=False)
    wut_data_blocks = Column(Integer, unique=False)

    #/////////////////////////////////////////////////////////
    # pedestal/ADC mean and RMS of TPC wires/channels
    #/////////////////////////////////////////////////////////
    tpc_pedestal_mean = Column(ARRAY(Float), unique=False)
    tpc_pedestal_rms = Column(ARRAY(Float), unique=False)

    #tpc_pedestal_samples_per_channel = Column(Integer, unique=False)
    #tpc_pedestal_acquisition_windows = Column(Integer, unique=False)

    tpc_adc_mean = Column(ARRAY(Float), unique=False)
    tpc_adc_rms = Column(ARRAY(Float), unique=False)

    #tpc_adc_samples_per_channel = Column(Integer, unique=False)
    #tpc_adc_acquisition_windows = Column(Integer, unique=False)

    #/////////////////////////////////////////////////////////
    # pedestal/ADC mean and RMS of CAEN boards
    #/////////////////////////////////////////////////////////
    caen_board_7_pedestal_mean = Column(ARRAY(Float), unique=False)  # V1740, last 32 channels of 64
    caen_board_8_pedestal_mean = Column(ARRAY(Float), unique=False)  # V1751, 8 channels
    caen_board_9_pedestal_mean = Column(ARRAY(Float), unique=False)  # V1751, 8 channels
    caen_board_24_pedestal_mean = Column(ARRAY(Float), unique=False)  # V1740B, 64 channels

    caen_board_7_pedestal_rms = Column(ARRAY(Float), unique=False)  # V1740, last 32 channels of 64
    caen_board_8_pedestal_rms = Column(ARRAY(Float), unique=False)  # V1751, 8 channels
    caen_board_9_pedestal_rms = Column(ARRAY(Float), unique=False)  # V1751, 8 channels
    caen_board_24_pedestal_rms = Column(ARRAY(Float), unique=False)  # V1740B, 64 channels

    caen_board_7_adc_mean = Column(ARRAY(Float), unique=False)  # V1740, last 32 channels of 64
    caen_board_8_adc_mean = Column(ARRAY(Float), unique=False)  # V1751, 8 channels
    caen_board_9_adc_mean = Column(ARRAY(Float), unique=False)  # V1751, 8 channels
    caen_board_24_adc_mean = Column(ARRAY(Float), unique=False)  # V1740B, 64 channels

    caen_board_7_adc_rms = Column(ARRAY(Float), unique=False)  # V1740, last 32 channels of 64
    caen_board_8_adc_rms = Column(ARRAY(Float), unique=False)  # V1751, 8 channels
    caen_board_9_adc_rms = Column(ARRAY(Float), unique=False)  # V1751, 8 channels
    caen_board_24_adc_rms = Column(ARRAY(Float), unique=False)  # V1740B, 64 channels

    #/////////////////////////////////////////////////////////
    # histogram of pedestal/ADC values of CAEN V1751 boards
    #/////////////////////////////////////////////////////////
    caen_board_8_channel_0_adc_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_8_channel_1_adc_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_8_channel_2_adc_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_8_channel_3_adc_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_8_channel_4_adc_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_8_channel_5_adc_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_8_channel_6_adc_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_8_channel_7_adc_histogram_bins = Column(ARRAY(Integer), unique=False)

    caen_board_8_channel_0_adc_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_8_channel_1_adc_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_8_channel_2_adc_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_8_channel_3_adc_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_8_channel_4_adc_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_8_channel_5_adc_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_8_channel_6_adc_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_8_channel_7_adc_histogram_counts = Column(ARRAY(Integer), unique=False)

    caen_board_9_channel_0_adc_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_9_channel_1_adc_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_9_channel_2_adc_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_9_channel_3_adc_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_9_channel_4_adc_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_9_channel_5_adc_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_9_channel_6_adc_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_9_channel_7_adc_histogram_bins = Column(ARRAY(Integer), unique=False)

    caen_board_9_channel_0_adc_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_9_channel_1_adc_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_9_channel_2_adc_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_9_channel_3_adc_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_9_channel_4_adc_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_9_channel_5_adc_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_9_channel_6_adc_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_9_channel_7_adc_histogram_counts = Column(ARRAY(Integer), unique=False)

    caen_v1751_adc_histogram_min_bin = Column(Integer, unique=False)
    caen_v1751_adc_histogram_max_bin = Column(Integer, unique=False)
    caen_v1751_adc_histogram_bin_width = Column(Integer, unique=False)

    #/////////////////////////////////////////////////////////
    # histograms of MWPC hits channel occupancy; 64 channels per TDC
    #/////////////////////////////////////////////////////////
    # good hits
    mwpc_good_hits_channel_histogram = Column(ARRAY(Integer), unique=False)
    # bad hits
    mwpc_bad_hits_channel_histogram = Column(ARRAY(Integer), unique=False)

    #/////////////////////////////////////////////////////////
    # histograms of MWPC hits timing occupancy; 1024 time bins per TDC
    #/////////////////////////////////////////////////////////
    # good hits
    mwpc_good_hits_timing_histogram = Column(ARRAY(Integer), unique=False)
    # bad hits
    mwpc_bad_hits_timing_histogram = Column(ARRAY(Integer), unique=False)

    #/////////////////////////////////////////////////////////
    # histograms of USTOF/DSTOF hits
    #/////////////////////////////////////////////////////////
    ustof_hits_histogram_bins = Column(ARRAY(Integer), unique=False)
    ustof_hits_histogram_counts = Column(ARRAY(Integer), unique=False)
    ustof_hits_histogram_min_bin = Column(Float, unique=False)
    ustof_hits_histogram_max_bin = Column(Float, unique=False)
    ustof_hits_histogram_bin_width = Column(Float, unique=False)

    dstof_hits_histogram_bins = Column(ARRAY(Integer), unique=False)
    dstof_hits_histogram_counts = Column(ARRAY(Integer), unique=False)
    dstof_hits_histogram_min_bin = Column(Float, unique=False)
    dstof_hits_histogram_max_bin = Column(Float, unique=False)
    dstof_hits_histogram_bin_width = Column(Float, unique=False)

    #/////////////////////////////////////////////////////////
    # histogram of TOF
    #/////////////////////////////////////////////////////////
    tof_histogram_bins = Column(ARRAY(Float), unique=False)
    tof_histogram_counts = Column(ARRAY(Integer), unique=False)
    tof_histogram_min_bin = Column(Float, unique=False)
    tof_histogram_max_bin = Column(Float, unique=False)
    tof_histogram_bin_width = Column(Float, unique=False)

    #/////////////////////////////////////////////////////////
    # histogram of momenta reconstructed from MWPC
    #/////////////////////////////////////////////////////////
    mwpc_momentum_histogram_bins = Column(ARRAY(Float), unique=False)
    mwpc_momentum_histogram_counts = Column(ARRAY(Integer), unique=False)

class DataQualitySubRun(DataQualityMixin, Base):
    """ Data quality table for subruns. """

    # table name
    __tablename__ = 'subruns'
    __table_args__ = {'schema' : 'dqm'}

    # psql sequence for unique ID
    #id = Column(Integer, primary_key=True)

    # subrun number
    subrun = Column(Integer, unique=False)

    def __init__(self, run, subrun, date_time, date_time_added):
        self.run = run
        self.subrun = subrun
        self.date_time = date_time
        self.date_time_added = date_time_added
        self.date_time_updated = date_time_added

    def __repr__(self):
        return '<DataQualitySubRun %r>' % (self.date_time)

class DataQualityRun(DataQualityMixin, Base):
    """ Data quality table for runs. """

    # table name
    __tablename__ = 'runs'
    __table_args__ = {'schema' : 'dqm'}

    # psql sequence for unique ID
    #id = Column(Integer, primary_key=True)

    # list of subruns added to this run
    subruns = Column(ARRAY(Integer), unique=False)

    def __init__(self, run, date_time, date_time_added):
        self.run = run
        self.date_time = date_time
        self.date_time_added = date_time_added
        self.date_time_updated = date_time_added

    def __repr__(self):
        return '<DataQualityRun %r>' % (self.date_time)

