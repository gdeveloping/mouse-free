import os
from pyjavaproperties import Properties
import logging
import time
import sys


def build_config_logger(log_level, log_file_path):
    logger = logging.getLogger()

    logger.setLevel(log_level)

    # Create a console handler and a file handler
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(log_file_path)

    # Create a formatter and attach it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Attach the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def get_config_from_properties_file(config_file_name):
    p = Properties()
    config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), config_file_name)
    with open(config_file_path, 'r') as config_file:
        p.load(config_file)
    return p


def str_to_log_level(level_str):
    str_to_level = {
        'NOTSET': logging.NOTSET,
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    return str_to_level.get(level_str.upper(), logging.ERROR)


def get_timestamp_ms():
    return time.time() * 1000


def get_current_function_name():
    return sys._getframe(1).f_code.co_name


def is_valid_single_alpha(key):
    return len(str(key)) == 1 and str(key).isalpha()