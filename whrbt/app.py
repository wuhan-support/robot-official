import re
from werobot import WeRoBot
from werobot.client import Client as InformationClient #消息类
import pandas as pd
import glob
from config import *
from redis_connect import Connect
from db_connect import *
import os
import json2csv_realtime

def pushData():
    list=[]
    for i in os.listdir('jsons/'):
        if i.split('.')[ 0]!='latest':
            if i.split('.')[ 1 ]!='json':
                timestamp = float(i.split('.')[ 0 ]+'.'+i.split('.')[ 1 ])
                list.append(timestamp)
    a=max(list)
    realtime_name=str(a)+'.json'
    json2csv_realtime.save_csv_area(realtime_name)
         
    df=pd.read_csv("csvs/real_time.csv",encoding="gbk")
    df=df.set_index("city")
    df=df.applymap(lambda x:str(x))
    series="confirmed:"+df["confirmed"]+" suspected:"+df["suspected"]+" cured:"+df["cured"]+" dead:"+df["dead"]
    return series
# 初始化
r = Connect(host=REDIS_HOST, port=REDIS_PORT)


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
        self.client.send_template_message(user_id, template_id, data, url)
    
    
class RedisToMySQL:
    """
    将Redis的内容每过一段时间更新进MySQL
    """
    raise NotImplementedError


# 文字消息处理句柄
@robot.text
def reply_text(message):
    wechat_id = message.source
    sub_city = re.compile("sub(.*)")
    pop_city = re.compile("pop(.*)")

    if sub_city:
        r.addUser(sub_city, wechat_id)
        return "订阅成功"
    
    if pop_city:
        r.deleteUser(pop_city, wechat_id)
        return "删除成功"
    
    return ""


# 订阅消息处理句柄
@robot.subscribe
def account_subscribe(message):
    return "感谢关注"


if __name__ == "main":
    robot = WeRoBot(token=TOKEN)
    robot.run(ROBOT_HOST, port=ROBOT_PORT)
