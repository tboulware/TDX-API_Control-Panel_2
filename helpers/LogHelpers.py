import logging
import os
from helpers.StringHelpers import StringHelpers

class LogHelpers(object):
    """description of class"""

    format = '%(asctime)s :: %(levelname)s :: %(message)s'
    fileName = 'appInfo.log'
    mode = 'w'
    level = 'INFO'
    rootFolder = 'logfiles'
  
    @classmethod
    def setConfiguration(cls, fileName=''):
        timeStr = StringHelpers.getDateTime()
        if fileName:
            cls.fileName = fileName
        logPath = os.getcwd() + '\\' + cls.rootFolder + '\\' + cls.fileName + '_' + timeStr + '.log'
        logging.basicConfig(filename = logPath, 
                            filemode= cls.mode, 
                            format=cls.format, 
                            level=logging.INFO)
        print(f'{cls.fileName} opened for logging')

    @classmethod
    def critical(cls, message):
        print(message)
        logging.critical(message)

    @classmethod
    def error(cls, message):
        print(message)
        logging.error(message)

    @classmethod
    def info(cls, message):
        print(message)
        logging.info(message)

    @classmethod 
    def warning(cls, message):
        print(message)
        logging.warning(message)

    @classmethod
    def debug(cls, message):
        #print(message)
        logging.debug(message)

    @classmethod
    def displayHeader(cls, message):
        print('\n' + message)
        print('________________________________________________\n')

    @classmethod
    def displayDetail(cls, message):
        print(message)

    @classmethod
    def displaySeparator(cls):
         print('________________________________________________')