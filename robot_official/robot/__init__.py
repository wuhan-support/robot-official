from time import sleep

from .constants import UPDATE_INTERVAL
from .push_updates import PushUpdatesClient


client = PushUpdatesClient()

def start_client():
    while True:
        sleep(UPDATE_INTERVAL + 1) # 为了尽可能避免两个线程在同时访问修改同一文件
        client.main()