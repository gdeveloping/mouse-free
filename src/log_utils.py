
from utils import *
from properties import *

# logger
logger = build_config_logger(LOG_LEVEL, LOG_FILE_PATH)


def log_function_name_to_enter():
    logger.debug('enter function: {}'.format(sys._getframe(1).f_code.co_name))


def log_function_name_to_exit():
    logger.debug('exit function: {}'.format(sys._getframe(1).f_code.co_name))

