from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.dialects.postgresql import ARRAY, BOOLEAN

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
    # number of events
    #/////////////////////////////////////////////////////////
    number_events = Column(Integer, unique=False)
    number_tpc_events = Column(Integer, unique=False)

    #/////////////////////////////////////////////////////////
    # number of data blocks
    #/////////////////////////////////////////////////////////
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
    mwc_data_blocks = Column(Integer, unique=False)
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
    # CAEN board 8
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

    caen_board_8_channel_0_adc_histogram_min_bin = Column(Integer, unique=False)
    caen_board_8_channel_1_adc_histogram_min_bin = Column(Integer, unique=False)
    caen_board_8_channel_2_adc_histogram_min_bin = Column(Integer, unique=False)
    caen_board_8_channel_3_adc_histogram_min_bin = Column(Integer, unique=False)
    caen_board_8_channel_4_adc_histogram_min_bin = Column(Integer, unique=False)
    caen_board_8_channel_5_adc_histogram_min_bin = Column(Integer, unique=False)
    caen_board_8_channel_6_adc_histogram_min_bin = Column(Integer, unique=False)
    caen_board_8_channel_7_adc_histogram_min_bin = Column(Integer, unique=False)

    caen_board_8_channel_0_adc_histogram_max_bin = Column(Integer, unique=False)
    caen_board_8_channel_1_adc_histogram_max_bin = Column(Integer, unique=False)
    caen_board_8_channel_2_adc_histogram_max_bin = Column(Integer, unique=False)
    caen_board_8_channel_3_adc_histogram_max_bin = Column(Integer, unique=False)
    caen_board_8_channel_4_adc_histogram_max_bin = Column(Integer, unique=False)
    caen_board_8_channel_5_adc_histogram_max_bin = Column(Integer, unique=False)
    caen_board_8_channel_6_adc_histogram_max_bin = Column(Integer, unique=False)
    caen_board_8_channel_7_adc_histogram_max_bin = Column(Integer, unique=False)

    caen_board_8_channel_0_adc_histogram_bin_width = Column(Integer, unique=False)
    caen_board_8_channel_1_adc_histogram_bin_width = Column(Integer, unique=False)
    caen_board_8_channel_2_adc_histogram_bin_width = Column(Integer, unique=False)
    caen_board_8_channel_3_adc_histogram_bin_width = Column(Integer, unique=False)
    caen_board_8_channel_4_adc_histogram_bin_width = Column(Integer, unique=False)
    caen_board_8_channel_5_adc_histogram_bin_width = Column(Integer, unique=False)
    caen_board_8_channel_6_adc_histogram_bin_width = Column(Integer, unique=False)
    caen_board_8_channel_7_adc_histogram_bin_width = Column(Integer, unique=False)

    caen_board_8_channel_0_adc_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_8_channel_1_adc_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_8_channel_2_adc_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_8_channel_3_adc_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_8_channel_4_adc_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_8_channel_5_adc_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_8_channel_6_adc_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_8_channel_7_adc_histogram_bin_indices = Column(ARRAY(Integer), unique=False)

    caen_board_8_channel_0_adc_histogram_number_bins = Column(Integer, unique=False)
    caen_board_8_channel_1_adc_histogram_number_bins = Column(Integer, unique=False)
    caen_board_8_channel_2_adc_histogram_number_bins = Column(Integer, unique=False)
    caen_board_8_channel_3_adc_histogram_number_bins = Column(Integer, unique=False)
    caen_board_8_channel_4_adc_histogram_number_bins = Column(Integer, unique=False)
    caen_board_8_channel_5_adc_histogram_number_bins = Column(Integer, unique=False)
    caen_board_8_channel_6_adc_histogram_number_bins = Column(Integer, unique=False)
    caen_board_8_channel_7_adc_histogram_number_bins = Column(Integer, unique=False)

    # CAEN board 9
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

    caen_board_9_channel_0_adc_histogram_min_bin = Column(Integer, unique=False)
    caen_board_9_channel_1_adc_histogram_min_bin = Column(Integer, unique=False)
    caen_board_9_channel_2_adc_histogram_min_bin = Column(Integer, unique=False)
    caen_board_9_channel_3_adc_histogram_min_bin = Column(Integer, unique=False)
    caen_board_9_channel_4_adc_histogram_min_bin = Column(Integer, unique=False)
    caen_board_9_channel_5_adc_histogram_min_bin = Column(Integer, unique=False)
    caen_board_9_channel_6_adc_histogram_min_bin = Column(Integer, unique=False)
    caen_board_9_channel_7_adc_histogram_min_bin = Column(Integer, unique=False)

    caen_board_9_channel_0_adc_histogram_max_bin = Column(Integer, unique=False)
    caen_board_9_channel_1_adc_histogram_max_bin = Column(Integer, unique=False)
    caen_board_9_channel_2_adc_histogram_max_bin = Column(Integer, unique=False)
    caen_board_9_channel_3_adc_histogram_max_bin = Column(Integer, unique=False)
    caen_board_9_channel_4_adc_histogram_max_bin = Column(Integer, unique=False)
    caen_board_9_channel_5_adc_histogram_max_bin = Column(Integer, unique=False)
    caen_board_9_channel_6_adc_histogram_max_bin = Column(Integer, unique=False)
    caen_board_9_channel_7_adc_histogram_max_bin = Column(Integer, unique=False)

    caen_board_9_channel_0_adc_histogram_bin_width = Column(Integer, unique=False)
    caen_board_9_channel_1_adc_histogram_bin_width = Column(Integer, unique=False)
    caen_board_9_channel_2_adc_histogram_bin_width = Column(Integer, unique=False)
    caen_board_9_channel_3_adc_histogram_bin_width = Column(Integer, unique=False)
    caen_board_9_channel_4_adc_histogram_bin_width = Column(Integer, unique=False)
    caen_board_9_channel_5_adc_histogram_bin_width = Column(Integer, unique=False)
    caen_board_9_channel_6_adc_histogram_bin_width = Column(Integer, unique=False)
    caen_board_9_channel_7_adc_histogram_bin_width = Column(Integer, unique=False)

    caen_board_9_channel_0_adc_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_9_channel_1_adc_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_9_channel_2_adc_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_9_channel_3_adc_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_9_channel_4_adc_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_9_channel_5_adc_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_9_channel_6_adc_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_9_channel_7_adc_histogram_bin_indices = Column(ARRAY(Integer), unique=False)

    caen_board_9_channel_0_adc_histogram_number_bins = Column(Integer, unique=False)
    caen_board_9_channel_1_adc_histogram_number_bins = Column(Integer, unique=False)
    caen_board_9_channel_2_adc_histogram_number_bins = Column(Integer, unique=False)
    caen_board_9_channel_3_adc_histogram_number_bins = Column(Integer, unique=False)
    caen_board_9_channel_4_adc_histogram_number_bins = Column(Integer, unique=False)
    caen_board_9_channel_5_adc_histogram_number_bins = Column(Integer, unique=False)
    caen_board_9_channel_6_adc_histogram_number_bins = Column(Integer, unique=False)
    caen_board_9_channel_7_adc_histogram_number_bins = Column(Integer, unique=False)

    #/////////////////////////////////////////////////////////
    # histograms of data block timestamps
    #/////////////////////////////////////////////////////////
    caen_board_0_timestamps_histogram_bins = Column(ARRAY(Float), unique=False)
    caen_board_0_timestamps_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_0_timestamps_histogram_min_bin = Column(Float, unique=False)
    caen_board_0_timestamps_histogram_max_bin = Column(Float, unique=False)
    caen_board_0_timestamps_histogram_bin_width = Column(Float, unique=False)
    caen_board_0_timestamps_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_0_timestamps_histogram_number_bins = Column(Integer, unique=False)

    caen_board_1_timestamps_histogram_bins = Column(ARRAY(Float), unique=False)
    caen_board_1_timestamps_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_1_timestamps_histogram_min_bin = Column(Float, unique=False)
    caen_board_1_timestamps_histogram_max_bin = Column(Float, unique=False)
    caen_board_1_timestamps_histogram_bin_width = Column(Float, unique=False)
    caen_board_1_timestamps_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_1_timestamps_histogram_number_bins = Column(Integer, unique=False)

    caen_board_2_timestamps_histogram_bins = Column(ARRAY(Float), unique=False)
    caen_board_2_timestamps_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_2_timestamps_histogram_min_bin = Column(Float, unique=False)
    caen_board_2_timestamps_histogram_max_bin = Column(Float, unique=False)
    caen_board_2_timestamps_histogram_bin_width = Column(Float, unique=False)
    caen_board_2_timestamps_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_2_timestamps_histogram_number_bins = Column(Integer, unique=False)

    caen_board_3_timestamps_histogram_bins = Column(ARRAY(Float), unique=False)
    caen_board_3_timestamps_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_3_timestamps_histogram_min_bin = Column(Float, unique=False)
    caen_board_3_timestamps_histogram_max_bin = Column(Float, unique=False)
    caen_board_3_timestamps_histogram_bin_width = Column(Float, unique=False)
    caen_board_3_timestamps_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_3_timestamps_histogram_number_bins = Column(Integer, unique=False)

    caen_board_4_timestamps_histogram_bins = Column(ARRAY(Float), unique=False)
    caen_board_4_timestamps_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_4_timestamps_histogram_min_bin = Column(Float, unique=False)
    caen_board_4_timestamps_histogram_max_bin = Column(Float, unique=False)
    caen_board_4_timestamps_histogram_bin_width = Column(Float, unique=False)
    caen_board_4_timestamps_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_4_timestamps_histogram_number_bins = Column(Integer, unique=False)

    caen_board_5_timestamps_histogram_bins = Column(ARRAY(Float), unique=False)
    caen_board_5_timestamps_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_5_timestamps_histogram_min_bin = Column(Float, unique=False)
    caen_board_5_timestamps_histogram_max_bin = Column(Float, unique=False)
    caen_board_5_timestamps_histogram_bin_width = Column(Float, unique=False)
    caen_board_5_timestamps_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_5_timestamps_histogram_number_bins = Column(Integer, unique=False)

    caen_board_6_timestamps_histogram_bins = Column(ARRAY(Float), unique=False)
    caen_board_6_timestamps_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_6_timestamps_histogram_min_bin = Column(Float, unique=False)
    caen_board_6_timestamps_histogram_max_bin = Column(Float, unique=False)
    caen_board_6_timestamps_histogram_bin_width = Column(Float, unique=False)
    caen_board_6_timestamps_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_6_timestamps_histogram_number_bins = Column(Integer, unique=False)

    caen_board_7_timestamps_histogram_bins = Column(ARRAY(Float), unique=False)
    caen_board_7_timestamps_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_7_timestamps_histogram_min_bin = Column(Float, unique=False)
    caen_board_7_timestamps_histogram_max_bin = Column(Float, unique=False)
    caen_board_7_timestamps_histogram_bin_width = Column(Float, unique=False)
    caen_board_7_timestamps_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_7_timestamps_histogram_number_bins = Column(Integer, unique=False)

    caen_board_8_timestamps_histogram_bins = Column(ARRAY(Float), unique=False)
    caen_board_8_timestamps_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_8_timestamps_histogram_min_bin = Column(Float, unique=False)
    caen_board_8_timestamps_histogram_max_bin = Column(Float, unique=False)
    caen_board_8_timestamps_histogram_bin_width = Column(Float, unique=False)
    caen_board_8_timestamps_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_8_timestamps_histogram_number_bins = Column(Integer, unique=False)

    caen_board_9_timestamps_histogram_bins = Column(ARRAY(Float), unique=False)
    caen_board_9_timestamps_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_9_timestamps_histogram_min_bin = Column(Float, unique=False)
    caen_board_9_timestamps_histogram_max_bin = Column(Float, unique=False)
    caen_board_9_timestamps_histogram_bin_width = Column(Float, unique=False)
    caen_board_9_timestamps_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_9_timestamps_histogram_number_bins = Column(Integer, unique=False)

    caen_board_24_timestamps_histogram_bins = Column(ARRAY(Float), unique=False)
    caen_board_24_timestamps_histogram_counts = Column(ARRAY(Integer), unique=False)
    caen_board_24_timestamps_histogram_min_bin = Column(Float, unique=False)
    caen_board_24_timestamps_histogram_max_bin = Column(Float, unique=False)
    caen_board_24_timestamps_histogram_bin_width = Column(Float, unique=False)
    caen_board_24_timestamps_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    caen_board_24_timestamps_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_timestamps_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_timestamps_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_timestamps_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_timestamps_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_timestamps_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_timestamps_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_timestamps_histogram_number_bins = Column(Integer, unique=False)

    wut_timestamps_histogram_bins = Column(ARRAY(Float), unique=False)
    wut_timestamps_histogram_counts = Column(ARRAY(Integer), unique=False)
    wut_timestamps_histogram_min_bin = Column(Float, unique=False)
    wut_timestamps_histogram_max_bin = Column(Float, unique=False)
    wut_timestamps_histogram_bin_width = Column(Float, unique=False)
    wut_timestamps_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    wut_timestamps_histogram_number_bins = Column(Integer, unique=False)

    #/////////////////////////////////////////////////////////
    # histograms of MWC hits channel occupancy; 64 channels per TDC
    #/////////////////////////////////////////////////////////
    # good hits
    mwc_tdc_1_good_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_1_good_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_1_good_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_1_good_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_1_good_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_1_good_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_1_good_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_2_good_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_2_good_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_2_good_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_2_good_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_2_good_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_2_good_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_2_good_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_3_good_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_3_good_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_3_good_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_3_good_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_3_good_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_3_good_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_3_good_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_4_good_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_4_good_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_4_good_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_4_good_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_4_good_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_4_good_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_4_good_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_5_good_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_5_good_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_5_good_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_5_good_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_5_good_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_5_good_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_5_good_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_6_good_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_6_good_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_6_good_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_6_good_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_6_good_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_6_good_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_6_good_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_7_good_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_7_good_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_7_good_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_7_good_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_7_good_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_7_good_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_7_good_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_8_good_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_8_good_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_8_good_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_8_good_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_8_good_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_8_good_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_8_good_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_9_good_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_9_good_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_9_good_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_9_good_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_9_good_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_9_good_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_9_good_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_10_good_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_10_good_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_10_good_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_10_good_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_10_good_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_10_good_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_10_good_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_11_good_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_11_good_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_11_good_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_11_good_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_11_good_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_11_good_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_11_good_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_12_good_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_12_good_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_12_good_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_12_good_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_12_good_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_12_good_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_12_good_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_13_good_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_13_good_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_13_good_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_13_good_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_13_good_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_13_good_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_13_good_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_14_good_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_14_good_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_14_good_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_14_good_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_14_good_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_14_good_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_14_good_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_15_good_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_15_good_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_15_good_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_15_good_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_15_good_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_15_good_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_15_good_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_16_good_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_16_good_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_16_good_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_16_good_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_16_good_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_16_good_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_16_good_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    # bad hits
    mwc_tdc_1_bad_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_1_bad_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_1_bad_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_1_bad_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_1_bad_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_1_bad_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_1_bad_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_2_bad_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_2_bad_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_2_bad_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_2_bad_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_2_bad_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_2_bad_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_2_bad_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_3_bad_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_3_bad_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_3_bad_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_3_bad_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_3_bad_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_3_bad_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_3_bad_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_4_bad_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_4_bad_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_4_bad_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_4_bad_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_4_bad_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_4_bad_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_4_bad_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_5_bad_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_5_bad_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_5_bad_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_5_bad_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_5_bad_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_5_bad_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_5_bad_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_6_bad_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_6_bad_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_6_bad_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_6_bad_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_6_bad_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_6_bad_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_6_bad_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_7_bad_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_7_bad_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_7_bad_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_7_bad_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_7_bad_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_7_bad_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_7_bad_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_8_bad_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_8_bad_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_8_bad_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_8_bad_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_8_bad_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_8_bad_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_8_bad_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_9_bad_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_9_bad_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_9_bad_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_9_bad_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_9_bad_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_9_bad_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_9_bad_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_10_bad_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_10_bad_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_10_bad_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_10_bad_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_10_bad_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_10_bad_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_10_bad_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_11_bad_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_11_bad_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_11_bad_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_11_bad_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_11_bad_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_11_bad_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_11_bad_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_12_bad_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_12_bad_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_12_bad_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_12_bad_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_12_bad_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_12_bad_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_12_bad_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_13_bad_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_13_bad_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_13_bad_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_13_bad_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_13_bad_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_13_bad_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_13_bad_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_14_bad_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_14_bad_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_14_bad_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_14_bad_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_14_bad_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_14_bad_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_14_bad_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_15_bad_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_15_bad_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_15_bad_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_15_bad_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_15_bad_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_15_bad_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_15_bad_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_16_bad_hits_channel_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_16_bad_hits_channel_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_16_bad_hits_channel_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_16_bad_hits_channel_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_16_bad_hits_channel_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_16_bad_hits_channel_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_16_bad_hits_channel_histogram_number_bins = Column(Integer, unique=False)

    #/////////////////////////////////////////////////////////
    # histograms of MWC hits timing occupancy; 1024 time bins per TDC
    #/////////////////////////////////////////////////////////
    # good hits
    mwc_tdc_1_good_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_1_good_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_1_good_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_1_good_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_1_good_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_1_good_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_1_good_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_2_good_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_2_good_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_2_good_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_2_good_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_2_good_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_2_good_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_2_good_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_3_good_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_3_good_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_3_good_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_3_good_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_3_good_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_3_good_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_3_good_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_4_good_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_4_good_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_4_good_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_4_good_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_4_good_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_4_good_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_4_good_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_5_good_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_5_good_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_5_good_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_5_good_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_5_good_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_5_good_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_5_good_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_6_good_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_6_good_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_6_good_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_6_good_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_6_good_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_6_good_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_6_good_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_7_good_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_7_good_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_7_good_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_7_good_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_7_good_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_7_good_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_7_good_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_8_good_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_8_good_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_8_good_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_8_good_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_8_good_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_8_good_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_8_good_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_9_good_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_9_good_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_9_good_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_9_good_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_9_good_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_9_good_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_9_good_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_10_good_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_10_good_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_10_good_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_10_good_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_10_good_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_10_good_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_10_good_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_11_good_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_11_good_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_11_good_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_11_good_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_11_good_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_11_good_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_11_good_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_12_good_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_12_good_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_12_good_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_12_good_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_12_good_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_12_good_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_12_good_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_13_good_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_13_good_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_13_good_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_13_good_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_13_good_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_13_good_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_13_good_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_14_good_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_14_good_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_14_good_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_14_good_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_14_good_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_14_good_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_14_good_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_15_good_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_15_good_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_15_good_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_15_good_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_15_good_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_15_good_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_15_good_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_16_good_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_16_good_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_16_good_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_16_good_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_16_good_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_16_good_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_16_good_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    # bad hits
    mwc_tdc_1_bad_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_1_bad_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_1_bad_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_1_bad_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_1_bad_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_1_bad_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_1_bad_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_2_bad_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_2_bad_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_2_bad_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_2_bad_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_2_bad_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_2_bad_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_2_bad_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_3_bad_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_3_bad_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_3_bad_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_3_bad_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_3_bad_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_3_bad_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_3_bad_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_4_bad_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_4_bad_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_4_bad_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_4_bad_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_4_bad_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_4_bad_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_4_bad_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_5_bad_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_5_bad_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_5_bad_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_5_bad_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_5_bad_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_5_bad_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_5_bad_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_6_bad_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_6_bad_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_6_bad_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_6_bad_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_6_bad_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_6_bad_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_6_bad_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_7_bad_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_7_bad_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_7_bad_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_7_bad_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_7_bad_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_7_bad_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_7_bad_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_8_bad_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_8_bad_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_8_bad_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_8_bad_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_8_bad_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_8_bad_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_8_bad_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_9_bad_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_9_bad_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_9_bad_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_9_bad_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_9_bad_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_9_bad_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_9_bad_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_10_bad_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_10_bad_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_10_bad_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_10_bad_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_10_bad_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_10_bad_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_10_bad_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_11_bad_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_11_bad_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_11_bad_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_11_bad_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_11_bad_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_11_bad_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_11_bad_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_12_bad_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_12_bad_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_12_bad_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_12_bad_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_12_bad_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_12_bad_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_12_bad_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_13_bad_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_13_bad_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_13_bad_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_13_bad_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_13_bad_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_13_bad_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_13_bad_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_14_bad_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_14_bad_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_14_bad_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_14_bad_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_14_bad_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_14_bad_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_14_bad_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_15_bad_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_15_bad_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_15_bad_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_15_bad_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_15_bad_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_15_bad_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_15_bad_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    mwc_tdc_16_bad_hits_timing_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_tdc_16_bad_hits_timing_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_tdc_16_bad_hits_timing_histogram_min_bin = Column(Float, unique=False)
    mwc_tdc_16_bad_hits_timing_histogram_max_bin = Column(Float, unique=False)
    mwc_tdc_16_bad_hits_timing_histogram_bin_width = Column(Float, unique=False)
    mwc_tdc_16_bad_hits_timing_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_tdc_16_bad_hits_timing_histogram_number_bins = Column(Integer, unique=False)

    #/////////////////////////////////////////////////////////
    # histograms of USTOF/DSTOF hits
    #/////////////////////////////////////////////////////////
    ustof_hits_histogram_bins = Column(ARRAY(Integer), unique=False)
    ustof_hits_histogram_counts = Column(ARRAY(Integer), unique=False)
    ustof_hits_histogram_min_bin = Column(Float, unique=False)
    ustof_hits_histogram_max_bin = Column(Float, unique=False)
    ustof_hits_histogram_bin_width = Column(Float, unique=False)
    ustof_hits_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    ustof_hits_histogram_number_bins = Column(Integer, unique=False)

    dstof_hits_histogram_bins = Column(ARRAY(Integer), unique=False)
    dstof_hits_histogram_counts = Column(ARRAY(Integer), unique=False)
    dstof_hits_histogram_min_bin = Column(Float, unique=False)
    dstof_hits_histogram_max_bin = Column(Float, unique=False)
    dstof_hits_histogram_bin_width = Column(Float, unique=False)
    dstof_hits_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    dstof_hits_histogram_number_bins = Column(Integer, unique=False)

    #/////////////////////////////////////////////////////////
    # histogram of TOF
    #/////////////////////////////////////////////////////////
    tof_histogram_bins = Column(ARRAY(Float), unique=False)
    tof_histogram_counts = Column(ARRAY(Integer), unique=False)
    tof_histogram_min_bin = Column(Float, unique=False)
    tof_histogram_max_bin = Column(Float, unique=False)
    tof_histogram_bin_width = Column(Float, unique=False)
    tof_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    tof_histogram_number_bins = Column(Integer, unique=False)

    #/////////////////////////////////////////////////////////
    # histogram of momenta reconstructed from MWC
    #/////////////////////////////////////////////////////////
    mwc_momenta_histogram_bins = Column(ARRAY(Float), unique=False)
    mwc_momenta_histogram_counts = Column(ARRAY(Integer), unique=False)
    mwc_momenta_histogram_min_bin = Column(Float, unique=False)
    mwc_momenta_histogram_max_bin = Column(Float, unique=False)
    mwc_momenta_histogram_bin_width = Column(Float, unique=False)
    mwc_momenta_histogram_bin_indices = Column(ARRAY(Integer), unique=False)
    mwc_momenta_histogram_number_bins = Column(Integer, unique=False)

class DataQualitySubRun(DataQualityMixin, Base):
    """ Data quality table for sub-runs. """

    # table name
    __tablename__ = 'subruns'
    __table_args__ = {'schema' : 'dqm'}

    # psql sequence for unique ID
    #id = Column(Integer, primary_key=True)

    #/////////////////////////////////////////////////////////
    # sub-run number
    #/////////////////////////////////////////////////////////
    subrun = Column(Integer, unique=False)

    def __init__(self, run, subrun, date_time, date_time_added):
        self.run = run
        self.subrun = subrun
        self.date_time = date_time
        self.date_time_added = date_time_added
        self.date_time_updated = date_time_added

    def __repr__(self):
        return '<DataQualitySubRun %r>' % (self.id)

class DataQualityRun(DataQualityMixin, Base):
    """ Data quality table for runs. """

    # table name
    __tablename__ = 'runs'
    __table_args__ = {'schema' : 'dqm'}

    # psql sequence for unique ID
    #id = Column(Integer, primary_key=True)

    #/////////////////////////////////////////////////////////
    # list of sub-runs added to this run
    #/////////////////////////////////////////////////////////
    subruns = Column(ARRAY(Integer), unique=False)

    def __init__(self, run, date_time, date_time_added):
        self.run = run
        self.date_time = date_time
        self.date_time_added = date_time_added
        self.date_time_updated = date_time_added

    def __repr__(self):
        return '<DataQualityRun %r>' % (self.id)

class DataQualityLatest(Base):
    """ Data quality table for the latest run/sub-run. """

    # table name
    __tablename__ = 'latest'
    __table_args__ = {'schema' : 'dqm'}

    #/////////////////////////////////////////////////////////
    # psql sequence for unique ID
    #/////////////////////////////////////////////////////////
    id = Column(Integer, primary_key=True)

    #/////////////////////////////////////////////////////////
    # run, sub-run, and datetime
    #/////////////////////////////////////////////////////////
    run = Column(Integer, unique=False)
    subrun = Column(Integer, unique=False)
    date_time_updated = Column(
        DateTime(timezone=False), unique=False, nullable=False)

    def __init__(self, run, subrun, date_time_updated):
        self.run = run
        self.subrun = subrun
        self.date_time_updated = date_time_updated

    def __repr__(self):
        return '<DataQualityLatest %r>' % (self.id)

class FileProcessing(Base):
    """ Table for the file-processing queue. """

    # table name
    __tablename__ = 'file_processing'
    __table_args__ = {'schema' : 'dqm'}

    #/////////////////////////////////////////////////////////
    # psql sequence for unique ID
    #/////////////////////////////////////////////////////////
    id = Column(Integer, primary_key=True)

    #/////////////////////////////////////////////////////////
    # run, sub-run, and datetime
    #/////////////////////////////////////////////////////////
    run = Column(Integer, unique=False)
    subrun = Column(Integer, unique=False)
    date_time_added = Column(
        DateTime(timezone=False), unique=False, nullable=False)

    def __init__(self, run, subrun, date_time_added):
        self.run = run
        self.subrun = subrun
        self.date_time_added = date_time_added

    #/////////////////////////////////////////////////////////
    # file paths
    #/////////////////////////////////////////////////////////
    dropbox_file_path = Column(String, unique=False)
    pnfs_file_path = Column(String, unique=False)

    #/////////////////////////////////////////////////////////
    # miscellaneous
    #/////////////////////////////////////////////////////////
    number_attempts = Column(Integer, unique=False)
    process_id = Column(Integer, unique=False)

    def __repr__(self):
        return '<FileProcessing %r>' % (self.id)

