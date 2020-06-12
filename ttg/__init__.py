from os import getenv
from sys import stdout
import logging


# set up logging
logging_handler = logging.StreamHandler(stdout)
logging_handler.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.WARN, handlers=[logging_handler])
del logging_handler

# Logging level for TTG module can be controlled by an ENV var TTG_LOG_LEVEL
# If not specified it will default to WARNING
logging.getLogger(__name__).setLevel(getenv('TTG_LOG_LEVEL', 'WARNING'))
