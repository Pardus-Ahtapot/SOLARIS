# -*- coding: utf-8 -*-

import logging
import subprocess


class Filelogger():
    def __init__(self,name,formatter,file_path,file_mode):
        self.name = name
        self.formatter = formatter
        self.file_path = file_path
        self.file_mode = file_mode

    def send_log(self,log_level,message):
        logging.basicConfig(format=self.formatter,filename=self.file_path,filemode=self.file_mode,level=logging.DEBUG)
        if log_level == "debug":
            logging.debug(message)
        elif log_level == "info":
            logging.info(message)
        elif log_level == "critical":
            logging.critical(message)
        elif log_level == "warning":
            logging.warning(message)
        elif log_level == "error":
            logging.error(message)
        else:
            pass


def get_logger():
    logger = Filelogger("AHTAPOT-GKTS", '%(asctime)s %(name)s %(levelname)s %(message)s', "/var/log/ahtapot/ahtapot-ps.log", "a")
    return logger
