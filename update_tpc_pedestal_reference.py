#/////////////////////////////////////////////////////////////
# Name:      update_pedestal_reference.py
# Date:      22 February 2016
# Author:    Everybody is an author!
#/////////////////////////////////////////////////////////////

import sys
import argparse
import re
from string import printable
from datetime import datetime

from redis import Redis

if __name__ == '__main__':

    #/////////////////////////////////////////////////////////
    # argparse
    #/////////////////////////////////////////////////////////
    parser = argparse.ArgumentParser(
        description="Parse from LArIAT pedestal file (.dat).")
    parser.add_argument('file', type=str,
        help="path to LArIAT pedestal file (.dat)")
    args = parser.parse_args()

    #/////////////////////////////////////////////////////////
    # get pedestal run number
    #/////////////////////////////////////////////////////////
    run = (args.file.split('_')[-1].split('.')[0])

    #/////////////////////////////////////////////////////////
    # get current timestamp
    #/////////////////////////////////////////////////////////
    timestamp = datetime.now().strftime('%s')

    #/////////////////////////////////////////////////////////
    # parse file to get pedestal mean for TPC channels
    #/////////////////////////////////////////////////////////
    pedestal_mean = []

    with open(args.file) as f:
        for line in f.readlines():
            if re.search('[a-zA-Z]', line):
                continue
            if line in ['\n', '\r\n']:
                continue
            if '480-483    ' in line:
                break
            #if re.search('480-483    ', line):
            #    break
            #print line

            line_ = re.sub("[^{}]+".format(printable), "", line)

            #print line_[10:18], line_[28:36], line_[46:54], line_[64:72]

            pedestal_mean.append(float(line_[10:18].strip(' ')))
            pedestal_mean.append(float(line_[28:36].strip(' ')))
            pedestal_mean.append(float(line_[46:54].strip(' ')))
            pedestal_mean.append(float(line_[64:72].strip(' ')))

    print("Pedestal run %s" % run)

    #/////////////////////////////////////////////////////////
    # redis client instance
    #/////////////////////////////////////////////////////////
    redis = Redis(host='lariat-daq01', port=6379)

    # redis keys
    key_prefix = 'dqm/pedestal-reference/'
    pedestal_mean_key = key_prefix + 'pedestal_mean'

    # send commands in a pipeline to save on round-trip time
    p = redis.pipeline()
    p.set(key_prefix + 'timestamp', timestamp)
    p.set(key_prefix + 'run', run)
    p.delete(pedestal_mean_key)
    p.rpush(pedestal_mean_key, *pedestal_mean)
    p.execute()

