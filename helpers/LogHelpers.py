import logging
class LogHelpers(object):
    """description of class"""

    __configuration = '%(asctime)s :: %(levelname)s :: %(message)s'
    __fileName = 'app.log'
    __mode = 'w'
    __level = logging.DEBUG


    @classmethod
    def setConfiguration(cls, filename='app.log', mode='w', level=logging.DEBUG):
        cls.__fileName = filename
        cls.__mode = mode
        cls.__level = level
        logging.basicConfig(filename = cls.__fileName , filemode=cls.__mode, format=cls.__configuration)
        logging.level = cls.__level
        print(f'{cls.__fileName} opened for logging')

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
        print(message)
        logging.debug(message)


    




