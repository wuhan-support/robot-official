import time

from threading import Thread
import schedule

from robot_official import start_app
from robot_official.spider import tx_spider
from robot_official.robot import push_client
from robot_official.utils.log import Logger
from robot_official.config import UPDATE_INTERVAL


logger = Logger()
logger.info('重启 robot_official')

schedule.every(UPDATE_INTERVAL).minutes.do(tx_spider.main)
schedule.every(UPDATE_INTERVAL + 1).minutes.do(push_client.main)

Thread(target=start_app).start()

schedule.run_all()
while True:
    schedule.run_pending()
    time.sleep(1)
