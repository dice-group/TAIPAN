import logging
import logging.config
import os
import json

from taipan.Config.Pathes import loggingConfigJson

class Logger(object):
    def __init__(self):
        pass

    def getLogger(self, name):
        self.setupLogging()
        return logging.getLogger(name)

    def setupLogging(self):
        path = loggingConfigJson
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = json.load(f)
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)
