#/////////////////////////////////////////////////////////////
# Name:      update_metrics.py
# Date:      21 February 2016
# Author:    Everybody is an author!
#/////////////////////////////////////////////////////////////

import os
import sys
import argparse
import itertools
from datetime import datetime, timedelta

import numpy as np
from sqlalchemy import and_
from redis import Redis

from dqm.database import db_session
from dqm.models import DataQualitySubRun
import dqm.allowed as allowed

from metrics.binning import round_time, date_time_bins

import log

bin_width = 60  # seconds
number_bins = 960

key_prefix = 'dqm/metric/1min/'
tpc_pedestal_mean_reference_key = 'dqm/pedestal-reference/pedestal_mean'

parameters = [
    'run',
    'subrun',
    'number_events',
    'number_tpc_events',
    'caen_board_0_data_blocks',
    'caen_board_1_data_blocks',
    'caen_board_2_data_blocks',
    'caen_board_3_data_blocks',
    'caen_board_4_data_blocks',
    'caen_board_5_data_blocks',
    'caen_board_6_data_blocks',
    'caen_board_7_data_blocks',
    'caen_board_8_data_blocks',
    'caen_board_9_data_blocks',
    'caen_board_24_data_blocks',
    'mwc_data_blocks',
    'wut_data_blocks',
    ]

array_parameters_base = {
    'tpc_pedestal_mean'           : allowed.tpc_channels,
    'tpc_pedestal_rms'            : allowed.tpc_channels,
    #'tpc_adc_mean'                : allowed.tpc_channels,
    #'tpc_adc_rms'                 : allowed.tpc_channels,
    'caen_board_7_pedestal_mean'  : allowed.v1740_channels[:32],
    'caen_board_8_pedestal_mean'  : allowed.v1751_channels,
    'caen_board_9_pedestal_mean'  : allowed.v1751_channels,
    'caen_board_24_pedestal_mean' : allowed.v1740b_channels,
    'caen_board_7_pedestal_rms'   : allowed.v1740_channels[:32],
    'caen_board_8_pedestal_rms'   : allowed.v1751_channels,
    'caen_board_9_pedestal_rms'   : allowed.v1751_channels,
    'caen_board_24_pedestal_rms'  : allowed.v1740b_channels,
    #'caen_board_7_adc_mean'       : allowed.v1740_channels[:32],
    #'caen_board_8_adc_mean'       : allowed.v1751_channels,
    #'caen_board_9_adc_mean'       : allowed.v1751_channels,
    #'caen_board_24_adc_mean'      : allowed.v1740b_channels,
    #'caen_board_7_adc_rms'        : allowed.v1740_channels[:32],
    #'caen_board_8_adc_rms'        : allowed.v1751_channels,
    #'caen_board_9_adc_rms'        : allowed.v1751_channels,
    #'caen_board_24_adc_rms'       : allowed.v1740b_channels,
    }

array_parameters_channel_offset = {
    'tpc_pedestal_mean'           : 0,
    'tpc_pedestal_rms'            : 0,
    #'tpc_adc_mean'                : 0,
    #'tpc_adc_rms'                 : 0,
    'caen_board_7_pedestal_mean'  : 32,
    'caen_board_8_pedestal_mean'  : 0,
    'caen_board_9_pedestal_mean'  : 0,
    'caen_board_24_pedestal_mean' : 0,
    'caen_board_7_pedestal_rms'   : 32,
    'caen_board_8_pedestal_rms'   : 0,
    'caen_board_9_pedestal_rms'   : 0,
    'caen_board_24_pedestal_rms'  : 0,
    #'caen_board_7_adc_mean'       : 32,
    #'caen_board_8_adc_mean'       : 0,
    #'caen_board_9_adc_mean'       : 0,
    #'caen_board_24_adc_mean'      : 0,
    #'caen_board_7_adc_rms'        : 32,
    #'caen_board_8_adc_rms'        : 0,
    #'caen_board_9_adc_rms'        : 0,
    #'caen_board_24_adc_rms'       : 0,
    }

array_parameters = []

for parameter_base, channel_indices in array_parameters_base.iteritems():
    for channel_index in channel_indices:
        channel = channel_index + \
            array_parameters_channel_offset[parameter_base]
        parameter = parameter_base + '_channel_' + str(channel)
        array_parameters.append(parameter)

tpc_pedestal_deviation_parameters = [
    'tpc_pedestal_deviation_channel_' + str(channel)
    for channel in allowed.tpc_channels
    ]

null_key = key_prefix + 'null'
null_list = [ None ] * number_bins

def update():
    date_time = datetime(2016, 2, 18, 22, 30, 00)
    #date_time = datetime(2016, 2, 18, 21, 45, 0)

    # http://stackoverflow.com/questions/8542723/change-datetime-to-unix-time-stamp-in-python
    timestamp = date_time.strftime('%s')

    #/////////////////////////////////////////////////////////
    # redis client instance
    #/////////////////////////////////////////////////////////
    redis = Redis()

    # null array for empty horizon
    if not redis.exists(null_key):
        # send commands in a pipeline to save on round-trip time
        p = redis.pipeline()
        p.delete(null_key)
        p.rpush(null_key, *null_list)
        p.execute()
        
    # check if the TPC pedestal mean reference exists
    tpc_pedestal_reference_exists = redis.exists(
        tpc_pedestal_mean_reference_key)

    if tpc_pedestal_reference_exists:
        tpc_pedestal_mean_reference = redis.lrange(
            tpc_pedestal_mean_reference_key, 0, -1)

    #/////////////////////////////////////////////////////////
    # query PostgreSQL database
    #/////////////////////////////////////////////////////////
    query = db_session.query(DataQualitySubRun) \
        .order_by(DataQualitySubRun.date_time.desc()) \
        .filter(and_(DataQualitySubRun.date_time <= date_time))
    results = query.all()

    #/////////////////////////////////////////////////////////
    # create bins for time series
    #/////////////////////////////////////////////////////////
    time_bins = date_time_bins(date_time, bin_width, number_bins)

    parameters_dict = {}
    for parameter in parameters:
        parameters_dict[parameter] = { time_bin : 0 for time_bin in time_bins }

    array_parameters_dict = {}
    for parameter in array_parameters:
        array_parameters_dict[parameter] = {
            time_bin : 0 for time_bin in time_bins }

    tpc_pedestal_deviation_dict = {}
    for parameter in tpc_pedestal_deviation_parameters:
        tpc_pedestal_deviation_dict[parameter] = {
            time_bin : None for time_bin in time_bins }

    #/////////////////////////////////////////////////////////
    # place the results into the appropriate time bin
    #/////////////////////////////////////////////////////////
    for result in results:
        time_bin = round_time(result.date_time, bin_width)
        if time_bin not in time_bins:
            continue
        for parameter in parameters:
            attr = getattr(result, parameter)
            if not isinstance(attr, list):
                parameters_dict[parameter][time_bin] = attr

        for parameter_base, channel_indices in \
            array_parameters_base.iteritems():
            array = getattr(result, parameter_base)

            for channel_index in channel_indices:

                channel = channel_index + \
                          array_parameters_channel_offset[parameter_base]

                parameter = parameter_base + '_channel_' + str(channel)
                value = array[channel_index]
                array_parameters_dict[parameter][time_bin] = value

                if (parameter_base == 'tpc_pedestal_mean' and
                    tpc_pedestal_reference_exists):

                    parameter = 'tpc_pedestal_deviation_channel_' + \
                                str(channel)

                    if value > 0:
                        tpc_pedestal_deviation_dict[parameter][time_bin] = \
                            value - \
                            float(tpc_pedestal_mean_reference[channel_index])

    #/////////////////////////////////////////////////////////
    # sort according to datetime
    #/////////////////////////////////////////////////////////
    parameter_values = {}
    for parameter in parameters:
        parameter_values[parameter] = [
            x for (y, x) in sorted(zip(parameters_dict[parameter].keys(),
                                       parameters_dict[parameter].values()))
            ]

    array_parameter_values = {}
    for parameter in array_parameters:
        array_parameter_values[parameter] = [
            x for (y, x) in
            sorted(zip(array_parameters_dict[parameter].keys(),
                       array_parameters_dict[parameter].values()))
            ]

    tpc_pedestal_deviation_parameter_values = {}
    for parameter in tpc_pedestal_deviation_parameters:
        tpc_pedestal_deviation_parameter_values[parameter] = [
            x for (y, x) in
            sorted(zip(tpc_pedestal_deviation_dict[parameter].keys(),
                       tpc_pedestal_deviation_dict[parameter].values()))
            ]

    # send commands in a pipeline to save on round-trip time
    p = redis.pipeline()
    p.set(key_prefix + 'timestamp', timestamp)
    for parameter in parameters:
        parameter_key = key_prefix + parameter
        p.delete(parameter_key)
        p.rpush(parameter_key, *parameter_values[parameter])
    p.execute()

    # send commands in a pipeline to save on round-trip time
    p = redis.pipeline()
    for parameter in array_parameters:
        parameter_key = key_prefix + parameter
        p.delete(parameter_key)
        p.rpush(parameter_key, *array_parameter_values[parameter])
    p.execute()

    # send commands in a pipeline to save on round-trip time
    p = redis.pipeline()
    for parameter in tpc_pedestal_deviation_parameters:
        parameter_key = key_prefix + parameter
        p.delete(parameter_key)
        p.rpush(parameter_key,
                *tpc_pedestal_deviation_parameter_values[parameter])
    p.execute()

if __name__ == '__main__':

    update()

    db_session.close()
