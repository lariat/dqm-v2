#!/usr/bin/env python

import time
import socket
import subprocess
from datetime import datetime

import logging
#from logging.handlers import RotatingFileHandler

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from rq import Queue
from worker import conn

#from dqmproc import process_raw_data_file
import imp
dqmproc = imp.load_source(
    'dqmproc',
    '/home/nfs/lariatdqm/app/dqm-v2/dqm-v2/processes/dqmproc.py'
    )

hostname = socket.gethostname()

src_file_dir = '/daqdata/dropbox'
#log_file_path = '/lariat/data/users/lariatdqm/dqm-v2/log/cerberus.log'

msg_format = "[%(asctime)s] [%(name)s] [" \
             + hostname + \
             "] [%(process)d] [%(levelname)s] %(message)s"
date_format = '%Y-%m-%d %H:%M:%S'

formatter = logging.Formatter(
    fmt=msg_format,
    datefmt=date_format
    )

#handler = RotatingFileHandler(
#    filename=log_file_path,
#    mode='a',
#    maxBytes=50000000,
#    backupCount=10,
#    )

handler = logging.StreamHandler()

handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)

logger = logging.getLogger('cerberus')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

q = Queue(connection=conn, default_timeout=300)

class FileHandler(PatternMatchingEventHandler):
    patterns = [ src_file_dir + '/lariat_r*_sr*.root' ]

    def log(self, event):
        """
        event.event_type 
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """

        log_message = '%s file: %s' % (
            event.event_type.capitalize(),
            event.src_path
            )

        if hasattr(event, 'dest_path'):
            log_message += ' => %s' % event.dest_path

        logger.info(log_message)

    def process(self, event):

        if hasattr(event, 'dest_path'):
            src_file_path = event.dest_path
        else:
            src_file_path = event.src_path

        #result = q.enqueue(process_raw_data_file, src_file_path)
        result = q.enqueue(dqmproc.process_raw_data_file, src_file_path)

    def on_created(self, event):
        self.log(event)
        self.process(event)

    def on_modified(self, event):
        self.log(event)

    def on_deleted(self, event):
        self.log(event)

    def on_moved(self, event):
        self.log(event)
        self.process(event)

if __name__ == '__main__':

    observer = Observer()
    observer.schedule(FileHandler(), path=src_file_dir)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
