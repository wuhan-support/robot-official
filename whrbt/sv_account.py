from config import APP_ID,APP_SECRET,TEMPLATE_ID
from werobot.client import Client as InformationClient #消息类
from redis_connect import Connect
import random
import time
import pandas as pd
import os
import json2csv_realtime
import datetime
def pushData():
    tmp_list=[]
    for i in os.listdir('jsons/'):
        if i.split('.')[ 0]!='latest':
            if i.split('.')[ 1 ]!='json':
                timestamp = float(i.split('.')[ 0 ]+'.'+i.split('.')[ 1 ])
                tmp_list.append(timestamp)
    a=max(tmp_list)
    realtime_name=str(a)+'.json'
    json2csv_realtime.save_csv_area(realtime_name)
         
    df=pd.read_csv("csvs/real_time.csv",encoding="gbk")
    df=df.set_index("city")
    df=df.applymap(lambda x:str(x))
    series="confirmed:"+df["confirmed"]+" suspected:"+df["suspected"]+" cured:"+df["cured"]+" dead:"+df["dead"]
    return series

class CustomService:
    """
    客服服务，回复消息，根据city获取用户id，并发送
    """
    def __init__(self, APP_ID, APP_SECRET):
        config = {"APP_ID": APP_ID, "APP_SECRET": APP_SECRET}
        self.client = InformationClient(config)

    def add_custom_service_account(self, account, nickname, password):
        self.client.add_custom_service_account(account, nickname,password)

    def send_text_message(self, user_id, content):
        self.client.send_text_message(user_id, content)

    def send_template_message(self, user_id, template_id, data, url=""):
        self.client.send_template_message(user_id,template_id, data, url)


while True:
    time.sleep(10+10*random.random())
    city="武汉"
    series=pushData()
    data=series[city]
    r=Connect()
    client=CustomService(APP_ID,APP_SECRET)
    
    for wechat_id in r.getData(city.encode()):
        Data={
                    "Data":{
                        "value":data,
                        "color":"#173177"
                    },
                    "Date":{
                        "value":datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"),
                        "color":"#173177"
                    },
                    "City":{
                        "value":city,
                        "color":"#173177"
                    }
        }
        client.send_template_message(wechat_id,TEMPLATE_ID,Data)    
    