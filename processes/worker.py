#!/usr/bin/env python

import os
import argparse
from redis import Redis
from rq import Worker, Queue, Connection

# queue names to listen to
listen = ['high', 'default', 'low']

# redis connection
conn = Redis(host='lariat-daq04', port=6379)

if __name__ == '__main__':

    # parser
    parser = argparse.ArgumentParser(description="Start RQ worker.")
    parser.add_argument(
        '--listen', nargs='+', type=str, help="queue names to listen to")

    # parse parser arguments
    args = parser.parse_args()

    # if specified, override queue names to listen to
    if args.listen:
        listen = args.listen

    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
