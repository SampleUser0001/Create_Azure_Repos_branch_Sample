# -*- coding: utf-8 -*-
from logging import getLogger, config, StreamHandler, DEBUG
import os

from logutil import LogUtil

PYTHON_APP_HOME = os.getenv('PYTHON_APP_HOME')
LOG_CONFIG_FILE = ['config', 'log_config.json']

logger = getLogger(__name__)
log_conf = LogUtil.get_log_conf(os.path.join(PYTHON_APP_HOME, *LOG_CONFIG_FILE))
config.dictConfig(log_conf)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

class Util:
    @staticmethod
    def print():
        logger.info('Hello Util.')
        return 'This is Util'