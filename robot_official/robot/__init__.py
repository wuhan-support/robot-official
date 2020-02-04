from time import sleep

from .push_updates import PushUpdatesClient
from ..config import UPDATE_INTERVAL


client = PushUpdatesClient()

def start_client():
    while True:
        sleep(UPDATE_INTERVAL + 1) # 为了尽可能避免两个线程同时修改同一文件
        client.main()
