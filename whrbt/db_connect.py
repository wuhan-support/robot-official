import sqlite3
import requests


CITY_DATA_URL = 'https://raw.githubusercontent.com/wecatch/china_regions/master/json/city_object.json'


class SQLiteConnect:
    '''SQLite 数据库接口封装类'''

    def __init__(db_file):
        self.conn = sqlite3.connect(db_file)

    def get_cities_list():
        '''获取包含所有中国城市名称的列表'''
        pass

    def save_subscription(uid, city):
        '''保存一个用户对于制定城市的订阅'''
        pass

    def cancel_subscription(uid, city):
        '''取消一个用户对于指定城市的订阅'''
        pass

    def get_subscribed_users(city):
        '''获取所有订阅指定城市的用户'''
        pass
