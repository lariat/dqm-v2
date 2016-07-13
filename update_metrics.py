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

#from log import Logger

#log = Logger('update_metrics', './logs/update_metrics.log')

delay = 3 * 60  # seconds
bin_width = 60  # seconds
number_bins = 970 # 960

v1751_pedestal_reference = 1024/2.
v1740_pedestal_reference = 4096/2.
v1740b_pedestal_reference = 4096/2.

key_prefix = 'dqm/metric/1min/'
tpc_pedestal_mean_reference_key = 'dqm/pedestal-reference/pedestal_mean'
daq_uptime_key = 'dqm/daq/uptime'

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

caen_pedestal_deviation_parameters = []

caen_pedestal_deviation_parameters.extend([
    'caen_board_8_pedestal_deviation_channel_' + str(channel)
    for channel in allowed.v1751_channels
    ])

caen_pedestal_deviation_parameters.extend([
    'caen_board_9_pedestal_deviation_channel_' + str(channel)
    for channel in allowed.v1751_channels
    ])

caen_pedestal_deviation_parameters.extend([
    'caen_board_7_pedestal_deviation_channel_' + str(channel)
    for channel in allowed.v1740_channels[32:]
    ])

caen_pedestal_deviation_parameters.extend( [
    'caen_board_24_pedestal_deviation_channel_' + str(channel)
    for channel in allowed.v1740b_channels
    ])

null_key = key_prefix + 'null'
null_list = [ None ] * number_bins

def update():
    date_time = datetime.now() - timedelta(seconds=delay)

    # http://stackoverflow.com/questions/8542723/change-datetime-to-unix-time-stamp-in-python
    timestamp = date_time.strftime('%s')

    #/////////////////////////////////////////////////////////
    # redis client instance
    #/////////////////////////////////////////////////////////
    redis = Redis(host='lariat-daq01', port=6379)

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
    # create bins for time series
    #/////////////////////////////////////////////////////////
    time_bins = date_time_bins(date_time, bin_width, number_bins)
    date_time_start, date_time_stop = time_bins[0], time_bins[-1]

    # send commands in a pipeline to save on round-trip time
    p = redis.pipeline()
    time_bins_key = key_prefix + 'time_bins'
    p.delete(time_bins_key)
    p.rpush(time_bins_key, *time_bins)
    p.execute()

    #/////////////////////////////////////////////////////////
    # query PostgreSQL database
    #/////////////////////////////////////////////////////////
    #query = db_session.query(DataQualitySubRun) \
    #    .order_by(DataQualitySubRun.date_time.desc()) \
    #    .filter(and_(DataQualitySubRun.date_time <= date_time))
    query = db_session.query(DataQualitySubRun) \
        .order_by(DataQualitySubRun.date_time.desc()) \
        .filter(DataQualitySubRun.date_time.between(date_time_start,
                                                    date_time_stop))
    results = query.all()

    #/////////////////////////////////////////////////////////
    # initialize bins for time series
    #/////////////////////////////////////////////////////////
    parameters_dict = {}
    for parameter in parameters:
        parameters_dict[parameter] = {
            time_bin : None for time_bin in time_bins }

    array_parameters_dict = {}
    for parameter in array_parameters:
        array_parameters_dict[parameter] = {
            time_bin : None for time_bin in time_bins }

    tpc_pedestal_deviation_dict = {}
    for parameter in tpc_pedestal_deviation_parameters:
        tpc_pedestal_deviation_dict[parameter] = {
            time_bin : None for time_bin in time_bins }

    caen_pedestal_deviation_dict = {}
    for parameter in caen_pedestal_deviation_parameters:
        caen_pedestal_deviation_dict[parameter] = {
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
                    tpc_pedestal_reference_exists and value > 0):
                    parameter = 'tpc_pedestal_deviation_channel_' + \
                                str(channel)
                    tpc_pedestal_deviation_dict[parameter][time_bin] = \
                        value - \
                        float(tpc_pedestal_mean_reference[channel_index])

                if (parameter_base == 'caen_board_8_pedestal_mean' and
                    value > 0):
                    parameter = 'caen_board_8_pedestal_deviation_channel_' + \
                                str(channel)
                    caen_pedestal_deviation_dict[parameter][time_bin] = \
                        value - v1751_pedestal_reference

                if (parameter_base == 'caen_board_9_pedestal_mean' and
                    value > 0):
                    parameter = 'caen_board_9_pedestal_deviation_channel_' + \
                                str(channel)
                    caen_pedestal_deviation_dict[parameter][time_bin] = \
                        value - v1751_pedestal_reference

                if (parameter_base == 'caen_board_7_pedestal_mean' and
                    value > 0):
                    parameter = 'caen_board_7_pedestal_deviation_channel_' + \
                                str(channel)
                    caen_pedestal_deviation_dict[parameter][time_bin] = \
                        value - v1740_pedestal_reference

                if (parameter_base == 'caen_board_24_pedestal_mean' and
                    value > 0):
                    parameter = 'caen_board_24_pedestal_deviation_channel_' + \
                                str(channel)
                    caen_pedestal_deviation_dict[parameter][time_bin] = \
                        value - v1740b_pedestal_reference

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

    caen_pedestal_deviation_parameter_values = {}
    for parameter in caen_pedestal_deviation_parameters:
        caen_pedestal_deviation_parameter_values[parameter] = [
            x for (y, x) in
            sorted(zip(caen_pedestal_deviation_dict[parameter].keys(),
                       caen_pedestal_deviation_dict[parameter].values()))
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

    # send commands in a pipeline to save on round-trip time
    p = redis.pipeline()
    for parameter in caen_pedestal_deviation_parameters:
        parameter_key = key_prefix + parameter
        p.delete(parameter_key)
        p.rpush(parameter_key,
                *caen_pedestal_deviation_parameter_values[parameter])
    p.execute()

    # get DAQ uptime for the last bin_width * number_bins seconds
    daq_minute_count = 0
    for subrun in parameter_values['subrun']:
        if subrun:
            daq_minute_count += 1
    daq_uptime = float(daq_minute_count) / len(parameter_values['subrun'])
    redis.set(daq_uptime_key, daq_uptime)

if __name__ == '__main__':

    update()

    db_session.close()
