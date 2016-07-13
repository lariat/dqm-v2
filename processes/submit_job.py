#!/usr/bin/env python

import sys

from rq import Queue
from worker import conn

#q = Queue('low', connection=conn)
q = Queue(connection=conn)

if __name__ == '__main__':

    import argparse
    from dqmproc import process_raw_data_file

    # parser
    parser = argparse.ArgumentParser(description="Submit job.")
    parser.add_argument('file', type=str, help="raw data file path")

    # parse parser arguments
    args = parser.parse_args()

    # get parsed arguments
    file_path = args.file

    result = q.enqueue(process_raw_data_file, file_path)

