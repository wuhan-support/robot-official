import os
import time
import random
import datetime

import pandas as pd
from dispose_data import *
from upload_latest_json import  update_latest_data
import threading
from werobot.client import Client as InformationClient # 消息类
from db_connect import RedisConnect,SQLiteConnect
from config import APP_ID, APP_SECRET, TEMPLATE_ID


class CustomService:
    """
    客服服务，回复消息，根据city获取用户id，并发送
    """

    def __init__(self, APP_ID, APP_SECRET):
        config = {"APP_ID": APP_ID, "APP_SECRET": APP_SECRET}
        self.client = InformationClient(config)

    def add_custom_service_account(self, account, nickname, password):
        self.client.add_custom_service_account(account, nickname, password)

    def send_text_message(self, user_id, content):
        self.client.send_text_message(user_id, content)

    def send_template_message(self, user_id, template_id, data, url=""):
        self.client.send_template_message(user_id, template_id, data, url)


def pushData():
    """
    对确诊，治愈和死亡人数进行字符串拼接，并以城市为index，拼接的字符串作为value存储
    在series中并返回
    """
    df=get_latest_data()
    df=df.applymap(lambda x: str(x))
    df=df.set_index("city")
    series = "确诊:" + df["confirmed"] + " 治愈:" + df["cured"] + " 死亡:" + df["dead"]
    return series


def updateData(old_series, new_series):
    """
    判断数据是否更新，获得更新的series，并返回
    """
    # print("*" * 10)
    # print(new_series)
    # print("*" * 10)
    # print(old_series)
    update_list=[]
    old_cities=old_series.index
    new_cities=new_series.index
    diff_cities=list(set(new_cities)-set(old_cities))
    # print("ln"*10)
    # print(old_series)
    flag_list=(old_series!=new_series[old_cities]).values
    # print("1"*10)
    # print(flag_list)
    if len(diff_cities)>0:
        update_list.extend(diff_cities)
    update_cities=(old_series[flag_list]).index
    # print("ln1"*10)
    if len(update_cities)>0:
        update_list.extend(update_cities)
    # print("eo"*10)
    print(update_cities)
    if len(update_cities)>0:
        return new_series[update_cities]
    else:
        return pd.Series()

def main():
    """
    对更新的series进行推送，推送内容由官网定义的模板内容获得TEMPLATE_ID
    及send_template_message第三个参数传入的data而定，可以自定义，同时更改TEMPLATE_ID
    """
    old_series = pushData()
    r = RedisConnect()

    while True:
        time.sleep(10 + 10 * random.random())
        new_series = pushData()
        update_series = updateData(old_series, new_series)
        if len(update_series) >= 1:
            old_series = new_series
        all_keys = set(r.get_all_keys())
        print(all_keys)
        co_cities = set(update_series.index) & set(all_keys)
        # co_cities=all_keys #待注释
        print(all_keys)
        print(set(update_series.index))
        print(co_cities)
        # update_series=new_series #待注释
        client = CustomService(APP_ID, APP_SECRET)
        for city in co_cities:
            data = update_series[city]
            for wechat_id in r.get_subscribed_users(city):
                Data = {
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
                client.send_template_message(wechat_id, TEMPLATE_ID, Data)

threading.Thread(target=update_latest_data).start()#更新数据
main()