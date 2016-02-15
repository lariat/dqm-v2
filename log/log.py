import sys
import logging
#from datetime import datetime

msg_format = "%(asctime)s [%(process)d] [%(levelname)s] %(message)s"
date_format = "[%Y-%m-%d %H:%M:%S]"

formatter = logging.Formatter(
    fmt=msg_format,
    datefmt=date_format
    )

handler = logging.StreamHandler()

handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

#class Logger:
#    """ Create a logger. """
#    def __init__(self, logger_name):
#        self.logger = logging.getLogger(logger_name)
#        self.logger.addHandler(handler)
#        self.logger.setLevel(logging.DEBUG)
