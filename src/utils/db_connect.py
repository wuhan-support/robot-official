import redis

import os

import requests
import sqlalchemy as db


CITY_DATA_URL = 'https://raw.githubusercontent.com/wecatch/china_regions/master/json/city_object.json'


class SQLiteConnect:
    '''SQLite 数据库接口封装类'''

    def __init__(self, db_file):
        create_tables = not os.path.isfile(db_file)

        self.engine = db.create_engine('sqlite:///{}'.format(db_file))
        self.conn = self.engine.connect()
        self.metadata = db.MetaData()
        self.cities_list = []

        self.initialize_tables(create_tables)
        if create_tables:
            self.insert_cities_data()

    def initialize_tables(self, create_tables=False):
        '''初始化数据库表'''
        self.cities = db.Table('cities', self.metadata,
            db.Column('id', db.Integer(), primary_key=True, nullable=False),
            db.Column('cn_id', db.String(12)),
            db.Column('name', db.String(255), nullable=False),
            db.Column('abbr', db.String(255)),
            db.Column('province', db.String(255)),
        )

        self.subscriptions = db.Table('subscriptions', self.metadata,
            db.Column('id', db.Integer(), primary_key=True, nullable=False),
            db.Column('uid', db.String(255), nullable=False),
            db.Column('city_id', db.Integer(), db.ForeignKey('cities.id'), nullable=False),
        )

        if create_tables:
            self.metadata.create_all(self.engine)
 
    def insert_cities_data(self):
        '''处理并将城市数据保存至数据库中'''
        raw_cities = self._get_all_cities()

        insert_data = []
        for city in raw_cities:
            row = {'cn_id': city['id']}
            if city['province'].endswith('市'):
                row['province'] = ''
                row['name'] = city['province']
                row['abbr'] = city['province'].rstrip('市')
            elif '直辖县级行政区划' in city['name']:
                continue
            else:
                row['province'] = city['province']
                row['name'] = city['name']
                row['abbr'] = city['name'].rstrip('市')
            insert_data.append(row)
        
        query = db.insert(self.cities)
        self.conn.execute(query, insert_data)

    def _get_all_cities(self):
        '''获取包含所有中国城市名称的列表'''
        try:
            req = requests.get(CITY_DATA_URL)
            if req.status_code != 200:
                return []
            data = req.json()
        except Exception:
            return []

        return [city_data for city_id, city_data in data.items()]
    
    def _get_city_id(self, city_name):
        '''获取指定城市名称在数据库中的ID'''
        # TODO: perhaps add fuzzy search?
        query = db.select([self.cities]).where(
            db.or_(
                self.cities.columns.abbr == city_name,
                self.cities.columns.name == city_name
            )
        )
        result_proxy = self.conn.execute(query)
        result = result_proxy.fetchone() # TODO: 处理城市重名情况
        if len(result) < 1:
            # 未找到城市名
            return -1
        city_id = result[0]
        return city_id

    def save_subscription(self, uid, city):
        '''保存一个用户对于制定城市的订阅'''
        # TODO: add feedback for invalid input
        city_id = self._get_city_id(city)
        if city_id == -1:
            return -1

        # 插入数据
        query = db.insert(self.subscriptions).values(uid=uid, city_id=city_id)
        self.conn.execute(query)

        return 0


    def cancel_subscription(self, uid, city):
        '''取消一个用户对于指定城市的订阅'''
        # TODO: add feedback for invalid input
        city_id = self._get_city_id(city)
        if city_id == -1:
            return -1
        
        # 检查是否存在这一订阅
        query = db.select([self.subscriptions]).where(
            db.and_(
                self.subscriptions.columns.uid == uid,
                self.subscriptions.columns.city_id == city_id
            )
        )
        result_proxy = self.conn.execute(query)
        result = result_proxy.fetchone()
        if not result:
            # 不存在这一订阅
            return -1 # TODO: Have a better and more consistent return code system

        # 删除数据
        # TODO: 这里一定要query两遍吗？
        query = db.delete(self.subscriptions).where(
            db.and_(
                self.subscriptions.columns.uid == uid,
                self.subscriptions.columns.city_id == city_id
            )
        )
        self.conn.execute(query)

        return 0

    def get_subscribed_users(self, city):
        '''获取所有订阅指定城市的用户'''
        # TODO: add feedback for invalid input
        city_id = self._get_city_id(city)
        if city_id == -1:
            return -1
        
        query = db.select([self.subscriptions]).where(self.subscriptions.columns.city_id == city_id)
        result_proxy = self.conn.execute(query)
        results = result_proxy.fetchall()

        return [sub[1] for sub in results]


class RedisConnect:
    """
    Redis 接口封装类
    """
    def __init__(self, host="localhost", port=6379, password=None):
        self.r = redis.Redis(host=host, port=port,decode_responses=True, password=password)

    def save_subscription(self, uid, city):
        self.r.sadd(city,uid)

    def cancel_subscription(self, uid, city):
        print(city)
        print(uid)
        self.r.srem(city, uid)
    
    def get_subscribed_users(self, city):
        return self.r.smembers(city)
    
    def get_all_keys(self):
        return self.r.keys()