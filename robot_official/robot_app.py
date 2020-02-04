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
logger = Logger('robot')

app = WeRoBot(token=TOKEN)
logger.info('初始化 WeRoBot 完成')

logger.info('数据库类型: {}'.format(DATABASE))
if DATABASE == 'redis':
    db = RedisConnect()
elif DATABASE == 'sqlite':
    db = SQLiteConnect()
else:
    logger.critical('未知数据库类型，无法初始化')
    exit()
logger.info('数据库初始化完成')


##### WeRoBot 句柄

# 文字消息处理句柄
@app.text
def reply_text(message):
    wechat_id = message.source
    msg = message.content

    if DATABASE == 'redis':
        data = Data(db)
        data_df = data.get_latest_data()
        all_city = data.get_all_city(data_df)
        pro_to_city = data.transfer_pro_to_ct(data_df)
        pros = pro_to_city.index
    
    # 这里存储订阅还可以使用微信官方提供的标签系统来实现
    # 但使用数据库无疑是对公众号影响最小的实现方法

    is_subscribe, target = is_subscribe_msg(msg)
    if is_subscribe:
        if not target:
            return '请输入地区名称（如：订阅武汉）。'
        # elif target in ('全国', '中国') or target in pros or target in all_city:
        #     db.save_subscription(wechat_id, target)
        #     return '成功订阅{}的疫情信息！'.format(target)
        code, sub_area_name = db.save_subscription(wechat_id, target)
        if code != -1:
            return '成功订阅{}的疫情信息！'.format(sub_area_name)
        else:
            return '尝试订阅{}失败，该地区名称不正确或暂无疫情信息。'.format(target)

    is_unsubscribe, target = is_unsubscribe_msg(msg)
    if is_unsubscribe:
        if not target:
            return '请输入地区名称（如：取消订阅武汉）。'
        # elif target in ('全国', '中国') or target in pros or target in all_city:
        #     db.cancel_subscription(wechat_id, target)
        #     return '成功取消{}的疫情信息订阅。'.format(target)
        elif db.cancel_subscription(wechat_id, target) != -1:
            return '成功取消{}的疫情信息订阅。'.format(target)
        else:
            return '尝试取消{}的疫情信息订阅失败，您好像没有订阅该地区信息或者地区名称错误。'.format(target)
    

    # if sub or can:
    #     # 本来是在监听时处理数据，现在换成推送时处理，单独形成数据处理
    #     if sub:
    #         sub = sub.group(1)
    #         print(sub)
    #         if sub in pros:
    #             #         for s in pro_to_city['city'][sub].split():
    #             r.save_subscription(wechat_id, sub)
    #             return '订阅成功%s' % (sub)
    #         elif sub == '全国':
    #             #         for s in all_city:
    #             r.save_subscription(wechat_id, sub)
    #             return '订阅成功%s' % (sub)
    #         elif sub in all_city:

    #             r.save_subscription(wechat_id, sub)
    #             return '订阅成功%s' % (sub)

    #         else:
    #             return '暂无该地区无法完成订阅'

    #     if can:
    #         can = can.group(1)
    #         print(can)
    #         if can in pros:
    #             #         for c in pro_to_city['city'][can].split():
    #             #             print(c)
    #             r.cancel_subscription(wechat_id, can)
    #             return '取消成功%s' % (can)
    #         elif can == '全国':
    #             #         for c in all_city:
    #             r.cancel_subscription(wechat_id, can)
    #             return '取消成功%s' % (can)
    #         elif can in all_city:
    #             r.cancel_subscription(wechat_id, can)
    #             return '取消成功%s' % (can)
    #         else:
    #             return '无法取消'

    return '输入有误，请重新输入'


# 订阅消息处理句柄
@app.subscribe
def account_subscribe(message):
    return '感谢关注'


##### 辅助函数

def is_subscribe_msg(msg):
    match = re.match(r'^(订阅)(.*)', msg)
    return match.groups() if match else (None, None)

def is_unsubscribe_msg(msg):
    match = re.match(r'^(取消(?:订阅)?)(.*)', msg)
    return match.groups() if match else (None, None)