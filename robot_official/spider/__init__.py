from time import sleep

from .tx_spider import TXSpider
from ..config import UPDATE_INTERVAL


tx_spider = TXSpider()

def start_spider():
    while True:
        tx_spider.main()
        sleep(UPDATE_INTERVAL)
