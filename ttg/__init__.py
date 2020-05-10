from os import getenv
from sys import stdout
import logging


# set up logging
__logging_handler = logging.StreamHandler(stdout)
__logging_handler.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.WARN, handlers=[__logging_handler])

# set up the root TTG logger
logging.getLogger(__name__).setLevel(getenv('TTG_LOG_LEVEL', 'WARNING'))
