from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
#from sqlalchemy.dialects.postgresql import HSTORE, JSON, JSONB
#from sqlalchemy.dialects import postgresql
#from sqlalchemy.ext.mutable import Mutable
#from sqlalchemy.ext.mutable import MutableDict

from dqm.database import Base

#class MutableList(Mutable, list):
#    def append(self, value):
#        list.append(self, value)
#        self.changed()
#
#    @classmethod
#    def coerce(cls, key, value):
#        if not isinstance(value, MutableList):
#            if isinstance(value, list):
#                return MutableList(value)
#            return Mutable.coerce(key, value)
#        else:
#            return value

class DataQualityMixin(object):
    """ Data quality mixin. """

    #/////////////////////////////////////////////////////////
    # psql sequence for unique ID
    #/////////////////////////////////////////////////////////
    id = Column(Integer, primary_key=True)

    #/////////////////////////////////////////////////////////
    # lariatsoft version; vAA_BB_CC
    #/////////////////////////////////////////////////////////
    #lariatsoft_version_a = Column(Integer, unique=False)
    #lariatsoft_version_b = Column(Integer, unique=False)
    #lariatsoft_version_c = Column(Integer, unique=False)

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
    #caen_board_0_pedestal_mean = Column(ARRAY(Float), unique=False)   # see TPC pedestal
    #caen_board_1_pedestal_mean = Column(ARRAY(Float), unique=False)   #
    #caen_board_2_pedestal_mean = Column(ARRAY(Float), unique=False)   #
    #caen_board_3_pedestal_mean = Column(ARRAY(Float), unique=False)   #
    #caen_board_4_pedestal_mean = Column(ARRAY(Float), unique=False)   #
    #caen_board_5_pedestal_mean = Column(ARRAY(Float), unique=False)   #
    #caen_board_6_pedestal_mean = Column(ARRAY(Float), unique=False)   #
    caen_board_7_pedestal_mean = Column(ARRAY(Float), unique=False)   # V1740, last 32 channels of 64
    caen_board_8_pedestal_mean = Column(ARRAY(Float), unique=False)   # V1751, 8 channels
    caen_board_9_pedestal_mean = Column(ARRAY(Float), unique=False)   # V1751, 8 channels
    caen_board_24_pedestal_mean = Column(ARRAY(Float), unique=False)  # V1740B, 64 channels

    #caen_board_0_pedestal_rms = Column(ARRAY(Float), unique=False)   # see TPC pedestal
    #caen_board_1_pedestal_rms = Column(ARRAY(Float), unique=False)   #
    #caen_board_2_pedestal_rms = Column(ARRAY(Float), unique=False)   #
    #caen_board_3_pedestal_rms = Column(ARRAY(Float), unique=False)   #
    #caen_board_4_pedestal_rms = Column(ARRAY(Float), unique=False)   #
    #caen_board_5_pedestal_rms = Column(ARRAY(Float), unique=False)   #
    #caen_board_6_pedestal_rms = Column(ARRAY(Float), unique=False)   #
    caen_board_7_pedestal_rms = Column(ARRAY(Float), unique=False)   # V1740, last 32 channels of 64
    caen_board_8_pedestal_rms = Column(ARRAY(Float), unique=False)   # V1751, 8 channels
    caen_board_9_pedestal_rms = Column(ARRAY(Float), unique=False)   # V1751, 8 channels
    caen_board_24_pedestal_rms = Column(ARRAY(Float), unique=False)  # V1740B, 64 channels

    #caen_v1740_pedestal_samples_per_channel = Column(Integer, unique=False)
    #caen_v1740_pedestal_acquisition_windows = Column(Integer, unique=False)

    #caen_v1751_pedestal_samples_per_channel = Column(Integer, unique=False)
    #caen_v1751_pedestal_acquisition_windows = Column(Integer, unique=False)

    #caen_v1740b_pedestal_samples_per_channel = Column(Integer, unique=False)
    #caen_v1740b_pedestal_acquisition_windows = Column(Integer, unique=False)

    #caen_board_0_adc_mean = Column(ARRAY(Float), unique=False)   # see TPC adc
    #caen_board_1_adc_mean = Column(ARRAY(Float), unique=False)   #
    #caen_board_2_adc_mean = Column(ARRAY(Float), unique=False)   #
    #caen_board_3_adc_mean = Column(ARRAY(Float), unique=False)   #
    #caen_board_4_adc_mean = Column(ARRAY(Float), unique=False)   #
    #caen_board_5_adc_mean = Column(ARRAY(Float), unique=False)   #
    #caen_board_6_adc_mean = Column(ARRAY(Float), unique=False)   #
    caen_board_7_adc_mean = Column(ARRAY(Float), unique=False)   # V1740, last 32 channels of 64
    caen_board_8_adc_mean = Column(ARRAY(Float), unique=False)   # V1751, 8 channels
    caen_board_9_adc_mean = Column(ARRAY(Float), unique=False)   # V1751, 8 channels
    caen_board_24_adc_mean = Column(ARRAY(Float), unique=False)  # V1740B, 64 channels

    #caen_board_0_adc_rms = Column(ARRAY(Float), unique=False)  # see TPC adc
    #caen_board_1_adc_rms = Column(ARRAY(Float), unique=False)  #
    #caen_board_2_adc_rms = Column(ARRAY(Float), unique=False)  #
    #caen_board_3_adc_rms = Column(ARRAY(Float), unique=False)  #
    #caen_board_4_adc_rms = Column(ARRAY(Float), unique=False)  #
    #caen_board_5_adc_rms = Column(ARRAY(Float), unique=False)  #
    #caen_board_6_adc_rms = Column(ARRAY(Float), unique=False)  #
    caen_board_7_adc_rms = Column(ARRAY(Float), unique=False)   # V1740, last 32 channels of 64
    caen_board_8_adc_rms = Column(ARRAY(Float), unique=False)   # V1751, 8 channels
    caen_board_9_adc_rms = Column(ARRAY(Float), unique=False)   # V1751, 8 channels
    caen_board_24_adc_rms = Column(ARRAY(Float), unique=False)  # V1740B, 64 channels

    #caen_v1740_adc_samples_per_channel = Column(Integer, unique=False)
    #caen_v1740_adc_acquisition_windows = Column(Integer, unique=False)

    #caen_v1751_adc_samples_per_channel = Column(Integer, unique=False)
    #caen_v1751_adc_acquisition_windows = Column(Integer, unique=False)

    #caen_v1740b_adc_samples_per_channel = Column(Integer, unique=False)
    #caen_v1740b_adc_acquisition_windows = Column(Integer, unique=False)

    #/////////////////////////////////////////////////////////
    # histogram of pedestal/ADC values in CAEN boards
    #/////////////////////////////////////////////////////////
    caen_board_0_pedestal_histogram = Column(ARRAY(Integer), unique=False)
    caen_board_1_pedestal_histogram = Column(ARRAY(Integer), unique=False)
    caen_board_2_pedestal_histogram = Column(ARRAY(Integer), unique=False)
    caen_board_3_pedestal_histogram = Column(ARRAY(Integer), unique=False)
    caen_board_4_pedestal_histogram = Column(ARRAY(Integer), unique=False)
    caen_board_5_pedestal_histogram = Column(ARRAY(Integer), unique=False)
    caen_board_6_pedestal_histogram = Column(ARRAY(Integer), unique=False)
    caen_board_7_pedestal_histogram = Column(ARRAY(Integer), unique=False)
    caen_board_8_pedestal_histogram = Column(ARRAY(Integer), unique=False)
    caen_board_9_pedestal_histogram = Column(ARRAY(Integer), unique=False)
    caen_board_24_pedestal_histogram = Column(ARRAY(Integer), unique=False)

    caen_board_0_adc_histogram = Column(ARRAY(Integer), unique=False)
    caen_board_1_adc_histogram = Column(ARRAY(Integer), unique=False)
    caen_board_2_adc_histogram = Column(ARRAY(Integer), unique=False)
    caen_board_3_adc_histogram = Column(ARRAY(Integer), unique=False)
    caen_board_4_adc_histogram = Column(ARRAY(Integer), unique=False)
    caen_board_5_adc_histogram = Column(ARRAY(Integer), unique=False)
    caen_board_6_adc_histogram = Column(ARRAY(Integer), unique=False)
    caen_board_7_adc_histogram = Column(ARRAY(Integer), unique=False)
    caen_board_8_adc_histogram = Column(ARRAY(Integer), unique=False)
    caen_board_9_adc_histogram = Column(ARRAY(Integer), unique=False)
    caen_board_24_adc_histogram = Column(ARRAY(Integer), unique=False)

    caen_board_0_pedestal_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_1_pedestal_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_2_pedestal_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_3_pedestal_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_4_pedestal_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_5_pedestal_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_6_pedestal_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_7_pedestal_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_8_pedestal_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_9_pedestal_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_24_pedestal_histogram_bins = Column(ARRAY(Integer), unique=False)

    caen_board_0_adc_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_1_adc_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_2_adc_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_3_adc_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_4_adc_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_5_adc_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_6_adc_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_7_adc_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_8_adc_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_9_adc_histogram_bins = Column(ARRAY(Integer), unique=False)
    caen_board_24_adc_histogram_bins = Column(ARRAY(Integer), unique=False)

    caen_board_0_pedestal_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_1_pedestal_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_2_pedestal_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_3_pedestal_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_4_pedestal_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_5_pedestal_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_6_pedestal_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_7_pedestal_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_8_pedestal_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_9_pedestal_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_24_pedestal_histogram_counts = Column(ARRAY(Integer), unique=False)

    caen_board_0_adc_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_1_adc_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_2_adc_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_3_adc_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_4_adc_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_5_adc_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_6_adc_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_7_adc_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_8_adc_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_9_adc_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_24_adc_histogram_counts = Column(ARRAY(Integer), unique=False)

    caen_v1740_pedestal_histograms_min_bin = Column(Integer, unique=False)
    caen_v1740_pedestal_histograms_max_bin = Column(Integer, unique=False)
    caen_v1740_pedestal_histograms_bin_width = Column(Integer, unique=False)

    caen_v1751_pedestal_histograms_min_bin = Column(Integer, unique=False)
    caen_v1751_pedestal_histograms_max_bin = Column(Integer, unique=False)
    caen_v1751_pedestal_histograms_bin_width = Column(Integer, unique=False)

    caen_v1740b_pedestal_histograms_min_bin = Column(Integer, unique=False)
    caen_v1740b_pedestal_histograms_max_bin = Column(Integer, unique=False)
    caen_v1740b_pedestal_histograms_bin_width = Column(Integer, unique=False)

    caen_v1740_adc_histograms_min_bin = Column(Integer, unique=False)
    caen_v1740_adc_histograms_max_bin = Column(Integer, unique=False)
    caen_v1740_adc_histograms_bin_width = Column(Integer, unique=False)

    caen_v1751_adc_histograms_min_bin = Column(Integer, unique=False)
    caen_v1751_adc_histograms_max_bin = Column(Integer, unique=False)
    caen_v1751_adc_histograms_bin_width = Column(Integer, unique=False)

    caen_v1740b_adc_histograms_min_bin = Column(Integer, unique=False)
    caen_v1740b_adc_histograms_max_bin = Column(Integer, unique=False)
    caen_v1740b_adc_histograms_bin_width = Column(Integer, unique=False)

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

