import itertools

#/////////////////////////////////////////////////////////////
# iterators for CAEN boards and channels
#/////////////////////////////////////////////////////////////
v1740_boards = range(0, 7+1)
v1751_boards = range(8, 9+1)
v1740b_boards = range(24, 24+1)
caen_boards = list(itertools.chain(v1740_boards, v1751_boards, v1740b_boards))
non_tpc_caen_boards = sorted(list(set(caen_boards) - set(v1740_boards[:-1])))

v1740_channels = range(64)
v1751_channels = range(8)
v1740b_channels = range(64)

#/////////////////////////////////////////////////////////////
# iterators for MWPC TDCs
#/////////////////////////////////////////////////////////////
mwpc_tdc_numbers = range(1, 16+1)
mwpc_tdc_channels = range(64)
mwpc_tdc_clock_ticks = range(1024)

#/////////////////////////////////////////////////////////////
# request args for Flask
#/////////////////////////////////////////////////////////////
request_args = {
    'number_events'            : None,
    'number_tpc_events'        : None,
    'number_data_blocks'       : {
        'device' : {
            'caen' : {
                'board' : caen_boards
                } 
            'mwpc' : None,
            'wut'  : None,
            }
        }
    'tpc_pedestal_mean_rms'    : None,
    'tpc_adc_mean_rms'         : None,
    'caen_pedestal_mean_rms'   : None,
    'caen_adc_mean_rms'        : None,
    'caen_v1751_adc_histogram' : {
        'board'   : v1751_boards,
        'channel' : v1751_channels,
        },
    'ustof_hits_histogram'     : None,
    'dstof_hits_histogram'     : None,
    'tof_histogram'            : None,
    'mwpc_hits_histogram'      : {
        'type'  : [ 'channel', 'timing' ],
        'class' : [ 'good'   , 'bad'    ],
        },
    'mwpc_momenta_histogram'   : None,
    }

