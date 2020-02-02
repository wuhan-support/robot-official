from time import sleep

from .constants import UPDATE_INTERVAL
from .tx_spider import TXSpider


tx_spider = TXSpider()

def start_spider():
    while True:
        tx_spider.main()
        sleep(UPDATE_INTERVAL)