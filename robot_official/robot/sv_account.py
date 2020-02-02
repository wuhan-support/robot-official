import os
import time
import random
import datetime
import threading

import pandas as pd
from werobot.client import Client as InformationClient

from .constants import ALL_CHINA
from .dispose_data import Data
from .upload_latest_json import update_latest_data
from ..utils.db_connect import RedisConnect, SQLiteConnect # 这里不应该要用到utils
from ..config import APP_ID, APP_SECRET, TEMPLATE_ID


class CustomService:
    '''客服服务，回复消息，根据city获取用户id，并发送'''

    def __init__(self, app_id, app_secret):
        config = {"APP_ID": app_id, "APP_SECRET": app_secret}
        self.client = InformationClient(config)

    def add_custom_service_account(self, account, nickname, password):
        self.client.add_custom_service_account(account, nickname, password)

    def send_text_message(self, user_id, content):
        self.client.send_text_message(user_id, content)

    def send_template_message(self, user_id, template_id, data, url=""):
        self.client.send_template_message(user_id, template_id, data, url)


def main():
    """
    对更新的series进行推送，推送内容由官网定义的模板内容获得TEMPLATE_ID
    及send_template_message第三个参数传入的data而定，可以自定义，同时更改TEMPLATE_ID
    """
    r = RedisConnect()
    old_data = Data(r)

    while True:
        time.sleep(100)
        new_data = Data(r)
        update_series, city_to_uid = old_data.updateData(new_data)
        if len(update_series) >= 1:
            old_data = new_data

        co_cities = list(city_to_uid.keys())
        print(set(update_series.index))
        print(co_cities)
        client = CustomService(APP_ID, APP_SECRET)
        for city in co_cities:
            data = update_series[city]
            for wechat_id in city_to_uid[city]:
                template_data = {
                    "Data": {
                        "value": data,
                        "color": "#173177"
                    },
                    "Date": {
                        "value": datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"),
                        "color": "#173177"
                    },
                    "City": {
                        "value": city,
                        "color": "#173177"
                    }
                }
                client.send_template_message(
                    wechat_id, TEMPLATE_ID, template_data)


threading.Thread(target=update_latest_data).start()  # 更新数据
main()
