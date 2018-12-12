import logging
import os

# log文件名字
log_file_name = "log-{}.log".format(os.getpid())


current_path = os.getcwd()
log = current_path + os.path.sep + 'log'
if not os.path.exists(log):
    os.mkdir(log)
name = log + os.path.sep + log_file_name


def getLogger():
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    # 文件操作句柄
    handler = logging.FileHandler(name)

    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '[%(asctime)s] - [%(filename)s] - [%(levelname)s] - [%(lineno)d] - %(message)s')
    # 添加log日志格式
    handler.setFormatter(formatter)
    # 前台操作句柄
    console = logging.StreamHandler()
    # 添加前台log日志的日志级别
    console.setLevel(logging.INFO)
    # 添加前台log日志格式
    console.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addHandler(console)
    return logger


logger = getLogger()
if __name__ == "__main__":
    logger.info("alsfalkjflajflka")
