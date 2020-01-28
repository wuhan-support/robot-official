import os
import re
import glob
from werobot import WeRoBot
import json2csv_realtime
from config import *
from db_connect import RedisConnect,SQLiteConnect


# 初始化
robot = WeRoBot(token=TOKEN)
r = RedisConnect(host=REDIS_HOST, port=REDIS_PORT)


class RedisToMySQL:
    """
    将Redis的内容每过一段时间更新进MySQL
    """
    pass


# 文字消息处理句柄
@robot.text
def reply_text(message):
    wechat_id = message.source
    print(message.content)
    sub_city = re.search("sub:(.*)",message.content)
    if sub_city:
        sub_city = sub_city.group(1)
        print(sub_city)
        r.save_subscription(wechat_id,sub_city)
        return "订阅成功"
    pop_city =re.search("pop:(.*)", message.content)
    if pop_city:
        pop_city = pop_city.group(1)
        r.cancel_subscription(wechat_id,pop_city)
        return "删除成功"
    return ""


# 订阅消息处理句柄
@robot.subscribe
def account_subscribe(message):
    return "感谢关注"


robot.run(ROBOT_HOST, port=ROBOT_PORT)
