import os
import re
import glob
from werobot import WeRoBot
from config import *
from db_connect import RedisConnect,SQLiteConnect
import json
import pandas as pd
from dispose_data import *
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
    data_df=get_latest_data()
    all_city=get_all_city(data_df)
    pro_to_city=transfer_pro_to_ct(data_df)
    pros=pro_to_city.index
    sub = re.search("订阅(.*)",message.content)
    can =re.search("取消(.*)", message.content)
    if sub or can:
            
        if sub:
            sub = sub.group(1)
            print(sub)
            if sub in pros:
                for s in pro_to_city["city"][sub].split():
                    r.save_subscription(wechat_id,s)
                return "订阅成功%s"%(sub)
            elif sub=="全国":
                for s in all_city:
                    r.save_subscription(wechat_id,s)
                return "订阅成功%s"%(sub)
            elif sub in all_city:
                
                r.save_subscription(wechat_id,sub)
                return "订阅成功%s"%(sub)
            
            else:
                return "暂无该地区无法完成订阅"
            
        if can:
            can = can.group(1)
            print(can)
            if can in pros:
                for c in pro_to_city["city"][can].split():
                    print(c)
                    r.cancel_subscription(wechat_id,c)
                return "取消成功%s"%(can)    
            elif can=="全国":
                for c in all_city:
                    r.cancel_subscription(wechat_id,c)
                return "取消成功%s"%(can)
            elif can in all_city:
                r.cancel_subscription(wechat_id,can)
                return "取消成功%s"%(can)
            else:
                return "无法取消"
                
    return "输入有误，请重新输入"

# 订阅消息处理句柄
@robot.subscribe
def account_subscribe(message):
    return "感谢关注"


robot.run(ROBOT_HOST, port=ROBOT_PORT)
