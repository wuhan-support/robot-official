from pathlib import Path

import redis
import sqlalchemy as sql

from .log import Logger
from ..config import SQLITE_FILE, REDIS_HOST, REDIS_PORT


logger = Logger('db')


class SQLiteConnect:
    '''SQLite 数据库接口封装类'''

    def __init__(self, db_file=SQLITE_FILE):
        create_tables = not Path(db_file).exists()

        # 目前机器人线程和爬虫线程都会访问同一个SQLite数据库
        # 这个操作会引起SQLite多线程错误警告
        # 目前，我使用了忽略警告的办法，但是这只是一个暂时性的解决方法
        # 未来需要更好的解决方法
        self.engine = sql.create_engine('sqlite:///{}'.format(db_file), connect_args={'check_same_thread': False})
        self.conn = self.engine.connect()
        self.metadata = sql.MetaData()
        self.areas_list = []

        self.initialize_tables(create_tables)
        # if create_tables:
        #     self.insert_cities_data()

    def initialize_tables(self, create_tables=False):
        '''初始化数据库表'''
        self.areas = sql.Table('cities', self.metadata,
            sql.Column('id', sql.Integer(), primary_key=True, nullable=False),
            sql.Column('name', sql.String(255)),
            sql.Column('abbr', sql.String(255)),
            sql.Column('suffix', sql.String(16)),
            sql.Column('parent', sql.String(255)),
        )

        self.subscriptions = sql.Table('subscriptions', self.metadata,
            sql.Column('id', sql.Integer(), primary_key=True, nullable=False),
            sql.Column('uid', sql.String(255), nullable=False),
            sql.Column('area_id', sql.Integer(), sql.ForeignKey('cities.id'), nullable=False),
        )

        if create_tables:
            self.metadata.create_all(self.engine)
            logger.info('数据库表创建完成')
 
    def get_all_areas(self):
        '''返回目前数据库中所有的地区名称'''
        query = sql.select([self.areas.columns.name])
        result_proxy = self.conn.execute(query)
        results = result_proxy.fetchall()

        return [area[0] for area in results]

    def save_area(self, abbr, suffix, parent):
        '''保存一个地区至数据库'''
        # TODO: 检查是否地区已经存在
        query = sql.insert(self.areas).values(abbr=abbr, suffix=suffix, name=abbr + suffix, parent=parent)
        self.conn.execute(query)
    
    def _get_city_id(self, city_name):
        '''获取指定城市名称在数据库中的ID'''
        # TODO: 可能可以添加模糊搜索
        # TODO: 使用缓存（或许Redis?）
        query = sql.select([self.areas]).where(
            sql.or_(
                self.areas.columns.abbr == city_name,
                self.areas.columns.name == city_name
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
        query = sql.insert(self.subscriptions).values(uid=uid, city_id=city_id)
        self.conn.execute(query)

        return 0

    def cancel_subscription(self, uid, city):
        '''取消一个用户对于指定城市的订阅'''
        # TODO: add feedback for invalid input
        city_id = self._get_city_id(city)
        if city_id == -1:
            return -1
        
        # 检查是否存在这一订阅
        query = sql.select([self.subscriptions]).where(
            sql.and_(
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
        query = sql.delete(self.subscriptions).where(
            sql.and_(
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
        
        query = sql.select([self.subscriptions]).where(self.subscriptions.columns.city_id == city_id)
        result_proxy = self.conn.execute(query)
        results = result_proxy.fetchall()

        return [sub[1] for sub in results]


class RedisConnect:
    '''Redis 数据库接口封装类'''

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=None):
        self.r = redis.Redis(host=host, port=port, decode_responses=True, password=password)

    def get_all_areas(self):
        '''返回目前数据库中所有的地区名称'''
        return self.r.keys('*')

    def save_area(self, abbr, suffix, parent):
        '''保存一个地区至数据库'''
        self.r.sadd('all_areas', abbr)
        self.r.sadd('all_areas', abbr + suffix)

    def save_subscription(self, uid, city):
        self.r.sadd(city, uid)

    def cancel_subscription(self, uid, city):
        print(city)
        print(uid)
        self.r.srem(city, uid)
    
    def get_subscribed_users(self, city):
        return self.r.smembers(city)
    
    def get_all_keys(self):
        return self.r.keys()
