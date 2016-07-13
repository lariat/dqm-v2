import logging
from logging.handlers import RotatingFileHandler

class Logger:
    """ Create a logger. """
    def __init__(self, logger_name, log_file_path):

        msg_format = "%(asctime)s [%(process)d] [%(levelname)s] %(message)s"
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

        self.logger = logging.getLogger(logger_name)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
