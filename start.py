from threading import Thread

from robot_official import start_app
from robot_official.spider import start_spider
from robot_official.utils.log import Logger


logger = Logger()


logger.info('重启 robot_official')

spider_thread = Thread(target=start_spider)
spider_thread.start()

start_app()
