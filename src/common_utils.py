import os
from pyjavaproperties import Properties
import logging
import time
import sys
import re
import json

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


def get_inner_config_file_dir_path():
    return os.path.dirname(os.path.realpath(__file__))


def get_executable_file_dir_path():
    return os.path.dirname(sys.executable)


def get_config_file_path(file_name):
    file_path = os.path.join(get_executable_file_dir_path(), file_name)
    if os.path.isfile(file_path):
        return file_path
    file_path = os.path.join(get_inner_config_file_dir_path(), file_name)
    return file_path


def get_config_properties(config_file_name):
    properties = Properties()
    config_file_path = get_config_file_path(config_file_name)
    with open(config_file_path, 'r') as config_file:
        properties.load(config_file)
    return properties


def get_config_hotkey(config_file_name):
    hotkeys = {}
    config_file_path = get_config_file_path(config_file_name)
    with open(config_file_path, 'r') as f:
        hotkeys = json.load(f)
    return hotkeys


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


def get_tuple_number_from_str(str):
    return tuple(map(int, re.findall(r'\d+', str)))