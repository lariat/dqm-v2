#!/usr/bin/env python

import socket
import subprocess

import logging
from logging.handlers import RotatingFileHandler

#///////////////////////////////////////////////////////////////////////
# configure logger
#///////////////////////////////////////////////////////////////////////
logger_name = 'metricsproc'
log_file_path = '/lariat/data/users/lariatdqm/dqm-v2/log/metricsproc/metricsproc.log'

msg_format = "%(asctime)s [%(name)s] [" \
             + socket.gethostname() + \
             "] [%(process)d] [%(levelname)s] %(message)s"
date_format = "[%Y-%m-%d %H:%M:%S]"

formatter = logging.Formatter(
    fmt=msg_format,
    datefmt=date_format
    )

handler = RotatingFileHandler(
    filename=log_file_path,
    mode='a',
    maxBytes=50000000,
    backupCount=10,
    )

#handler = logging.StreamHandler()

handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)

logger = logging.getLogger(logger_name)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def update_metrics():
    """
        Update metrics.
    """

    logger.info("Updating metrics...")

    command = [
        'python',
        '/home/nfs/lariatdqm/app/dqm-v2/dqm-v2/update_metrics.py',
        ]

    p = subprocess.check_call(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    logger.info("Updated metrics!")

    return p

