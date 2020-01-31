import os
import re
import json
import glob

import pandas as pd
from werobot import WeRoBot

from .config import *
from .utils.log import Logger
from .robot.dispose_data import Data
from .utils.db_connect import RedisConnect, SQLiteConnect


##### 初始化
logger = Logger()

logger.info('重启 robot_official')

app = WeRoBot(token=TOKEN)
logger.info('初始化 WeRoBot 完成')

logger.info('数据库类型: {}'.format(DATABASE))
if DATABASE == 'redis':
    r = RedisConnect(host=REDIS_HOST, port=REDIS_PORT)
elif DATABASE == 'sqlite':
    db = SQLiteConnect(db_file=SQLITE_FILE)
else:
    logger.critical('未知数据库类型，无法初始化')
    exit()
logger.info('数据库初始化完成')


##### WeRoBot 句柄

# 文字消息处理句柄
@app.text
def reply_text(message):
    # 获取消息相关信息
    wechat_id = message.source
    msg = message.content
    # print(message.content)
    data = Data(r)
    data_df = data.get_latest_data()
    all_city = data.get_all_city(data_df)
    pro_to_city = data.transfer_pro_to_ct(data_df)
    pros = pro_to_city.index
    sub = re.search('订阅(.*)', message.content)
    can = re.search('取消(.*)', message.content)

    is_subscribe, city = is_subscribe_msg(msg)
    if is_subscribe:
        pass

    is_unsubscribe, city = is_unsubscribe_msg(msg)
    if is_unsubscribe:
        pass
    

    if sub or can:
        # 本来是在监听时处理数据，现在换成推送时处理，单独形成数据处理
        if sub:
            sub = sub.group(1)
            print(sub)
            if sub in pros:
                #         for s in pro_to_city['city'][sub].split():
                r.save_subscription(wechat_id, sub)
                return '订阅成功%s' % (sub)
            elif sub == '全国':
                #         for s in all_city:
                r.save_subscription(wechat_id, sub)
                return '订阅成功%s' % (sub)
            elif sub in all_city:

                r.save_subscription(wechat_id, sub)
                return '订阅成功%s' % (sub)

            else:
                return '暂无该地区无法完成订阅'

        if can:
            can = can.group(1)
            print(can)
            if can in pros:
                #         for c in pro_to_city['city'][can].split():
                #             print(c)
                r.cancel_subscription(wechat_id, can)
                return '取消成功%s' % (can)
            elif can == '全国':
                #         for c in all_city:
                r.cancel_subscription(wechat_id, can)
                return '取消成功%s' % (can)
            elif can in all_city:
                r.cancel_subscription(wechat_id, can)
                return '取消成功%s' % (can)
            else:
                return '无法取消'

    return '输入有误，请重新输入'


# 订阅消息处理句柄
@app.subscribe
def account_subscribe(message):
    return '感谢关注'


##### 辅助函数

def is_subscribe_msg(msg):
    match = re.match(r'^订阅(.*)', msg)
    return match.groups() if match else (None, None)

def is_unsubscribe_msg(msg):
    match = re.match(r'^取消(?:订阅)?(.*)', msg)
    return match.groups() if match else (None, None)