
from common_utils import *
from properties import *
from functools import wraps


# logger
logger = build_config_logger(LOG_LEVEL, LOG_FILE_PATH)



def log_function_name_in_debug_level_to_enter_exit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug('enter function: {}'.format(func.__name__))
        res = func(*args, **kwargs)
        logger.debug('exit function: {}'.format(func.__name__))
        return res
    return wrapper

    
