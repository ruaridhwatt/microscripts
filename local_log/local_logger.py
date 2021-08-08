import logging
import logging.handlers as handlers

log_file_path = 'microscripts.log'

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logHandler = handlers.TimedRotatingFileHandler(log_file_path, when='D', interval=1, backupCount=2)
logHandler.setLevel(logging.INFO)
logHandler.setFormatter(formatter)


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(logHandler)
    return logger
