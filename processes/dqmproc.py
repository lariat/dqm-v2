#!/usr/bin/env python

import os
import sys
import time
import errno
import socket
import subprocess

import logging
from logging.handlers import RotatingFileHandler

import samweb_client

#///////////////////////////////////////////////////////////////////////
# configure logger
#///////////////////////////////////////////////////////////////////////
logger_name = 'dqmproc'
log_file_path = '/lariat/data/users/lariatdqm/dqm-v2/log/dqmproc/dqmproc.log'

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

#///////////////////////////////////////////////////////////////////////
# configure samweb
#///////////////////////////////////////////////////////////////////////
samweb = samweb_client.SAMWebClient(experiment='lariat')

def raw_file_path_from_sam(file_name):
    """
        Returns file path of raw data art ROOT file from SAM given a
        file name. An exception is raised of the file does not exist.
    """

    file_path_dict = samweb.locateFile(file_name)
    system = file_path_dict[0]['system']
    file_path = \
        file_path_dict[0]['full_path'].split(system + ':')[1] \
        + '/' + file_name
    return file_path

def file_exists(file_path):
    return os.path.isfile(file_path)

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def dqm_file_path_from_raw_file(
        raw_file_path,
        prefix='/lariat/data/users/lariatdqm/dqm-v2/files',
        check_path=True,
        debug=True):
    """
        Returns a path based on the run and sub-run numbers of the
        raw data art ROOT file.
    """

    # get raw data file name
    raw_file_name = raw_file_path.split('/')[-1]

    # tokenize raw data file name
    tokens = raw_file_name.split('_')

    # get run and subrun from raw data file name
    run = tokens[-2][1:]
    subrun = tokens[-1].split('.')[0][2:]

    # generate subdirectory path based on run and subrun
    aa, bb, cc, dd = run[0:2], run[2:4], run[4:6], subrun[0:2]
    subdirectory = '/' + aa + '/' + bb + '/' + cc + '/' + dd

    # concatenate prefix and subdirectory for path
    path = prefix + subdirectory

    # generate DQM file name based on run and subrun
    file_name = 'dqm_r' + run + '_sr' + subrun + '.root'

    # full file path for DQM file
    file_path = path + '/' + file_name

    if debug:
        logger.debug("raw_file_path: %s" % raw_file_path)
        logger.debug("raw_file_name: %s" % raw_file_name)
        logger.debug("tokens:        %s" % tokens)
        logger.debug("run:           %s" % run)
        logger.debug("subrun:        %s" % subrun)
        logger.debug("prefix:        %s" % prefix)
        logger.debug("subdirectory:  %s" % subdirectory)
        logger.debug("file_name:     %s" % file_name)
        logger.debug("file_path:     %s" % file_path)

    if check_path:
        make_sure_path_exists(path)

    return file_path

def process_raw_data_file(raw_data_file_path):
    """
        Process raw data file, write out DQM data file, read DQM data
        to database.
    """

    dqm_file_path = dqm_file_path_from_raw_file(raw_data_file_path)

    logger.info("Checking for existence of raw data file: %s"
                % raw_data_file_path)

    # give rsync time to race...
    time.sleep(20)

    if not file_exists(raw_data_file_path):

        logger.info("Cannot find file: %s" % raw_data_file_path)
        logger.info("Checking /pnfs/lariat via SAM...")

        # get raw data file name
        raw_file_name = raw_data_file_path.split('/')[-1]

        # get raw data file name
        raw_data_file_path = raw_file_path_from_sam(raw_file_name)

    # log files for process 1
    stdout_log_1 = dqm_file_path + '.out.log.1'
    stderr_log_1 = dqm_file_path + '.err.log.1'

    # log files for process 2
    stdout_log_2 = dqm_file_path + '.out.log.2'
    stderr_log_2 = dqm_file_path + '.err.log.2'

    # process raw data file, write out DQM data file
    logger.info("Processing raw data file: %s" % raw_data_file_path)

    with open(stdout_log_1, 'w') as stdout, open(stderr_log_1, 'w') as stderr:

        command = [
            'lar',
            '-c',
            'data_quality.fcl',
            raw_data_file_path,
            '-T',
            dqm_file_path,
            ]

        p1 = subprocess.check_call(command, stdout=stdout, stderr=stderr)

    logger.debug("p1 exit status: %s", p1)

    logger.info("Log file: %s" % stdout_log_1)
    logger.info("Log file: %s" % stderr_log_1)

    logger.info("Output DQM file: %s" % dqm_file_path)

    # read DQM data from file to database
    with open(stdout_log_2, 'w') as stdout, open(stderr_log_2, 'w') as stderr:

        command = [
            'python',
            '/home/nfs/lariatdqm/app/dqm-v2/dqm-v2/process_root_file.py',
            dqm_file_path,
            ]

        p2 = subprocess.check_call(command, stdout=stdout, stderr=stderr)

    logger.debug("p2 exit status: %s", p2)

    logger.info("Log file: %s" % stdout_log_2)
    logger.info("Log file: %s" % stderr_log_2)

    logger.info("Added to database!")

    #/////////////////////////////////////////////////////////
    # this is for the live TPC event viewer
    #/////////////////////////////////////////////////////////
    event_viewer_file_path = '/lariat/data/users/lariatdqm/dqm-v2/eventviewer/latest_dqm_file_path.txt'
    event_viewer_file = open(event_viewer_file_path, 'w')
    event_viewer_file.write(dqm_file_path)
    event_viewer_file.close()
    #/////////////////////////////////////////////////////////

    return p1, p2

