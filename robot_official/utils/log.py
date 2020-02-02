import sys
import datetime
import logging
from pathlib import Path


##### 常量、初始化与辅助函数

ROOT_LOGGER_NAME = 'main'
LOG_DIR = Path('logs/')

LOG_DIR.mkdir(exist_ok=True)

def get_log_filename():
    '''返回当日日志文件路径字符串'''
    filename = datetime.datetime.now().strftime('%Y-%m-%d')
    return (LOG_DIR / '{}.log'.format(filename)).as_posix()


##### Logging 基本设置

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

# 设置输出至日志文件的 Handler
file_handler = logging.FileHandler(get_log_filename(), 'a', 'utf-8')
file_formatter = logging.Formatter('%(asctime)s %(name)-15s %(levelname)-8s %(message)s', '%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(file_formatter)
root_logger.addHandler(file_handler)

# 设置单独输出至终端的 Handler
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(name)-15s: %(levelname)-8s %(message)s')
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(console_formatter)
root_logger.addHandler(console_handler)


class Logger:
    '''Logger 的封装类'''

    def __init__(self, module_name=None):
        logger_name = ROOT_LOGGER_NAME
        if module_name != None:
            logger_name += '.{}'.format(module_name)
        self.logger = logging.getLogger(logger_name)

        self.logger.debug('成功创建 Logger: {}'.format(logger_name))
    
    def debug(self, msg):
        self.logger.debug(msg)
    
    def info(self, msg):
        self.logger.info(msg)
    
    def warning(self, msg):
        self.logger.warning(msg)
    
    def error(self, msg):
        self.logger.error(msg)
    
    def critical(self, msg):
        self.logger.critical(msg)
        logging.shutdown()
        sys.exit()
    
    def exception(self, err):
        self.exception(err)