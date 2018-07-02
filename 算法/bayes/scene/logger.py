import os
import logging
current_path = os.getcwd()
log = current_path + os.path.sep + 'log'
if not os.path.exists(log):
    os.mkdir(log)


def getLogger():
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler("{0}testBayes.log".format(log + os.path.sep))

    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    logger.addHandler(handler)
    logger.addHandler(console)
    return logger

logger = getLogger()