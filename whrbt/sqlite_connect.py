import sqlalchemy as sql

import requests


CITY_DATA_URL = 'https://raw.githubusercontent.com/wecatch/china_regions/master/json/city_object.json'


class SQLiteConnect:
    '''SQLite 数据库接口封装类'''

    def __init__(db_file):
        self.engine = sql.create_engine('sqlite:///{}'.format(db_file))
        self.conn = self.engine.connect()
        self.metadata = sql.MetaData()
        self.cities_list = []

        self.update_cities_list()
        self.create_tables()

    def create_tables(self):
        '''创建数据库表'''
        self.cities = db.Table('cities', metadata,
            db.Column('id', db.Integer(), primary_key=True, nullable=False),
            db.Column('cn_id', db.String(12)),
            db.Column('name', db.String(255), nullable=False),
            db.Column('province', db.String(255)),
        )

        self.subscriptions = db.Table('cities', metadata,
            db.Column('id', db.Integer(), primary_key=True, nullable=False),
            db.Column('uid', db.String(255), nullable=False),
            db.Column('city_id', db.Integer(), nullable=False, sql.ForeignKey('cities.id')),
        )

        metadata.create_all(engine)
 
    def update_cities_list(self):
        '''处理并更新城市列表'''
        raw_cities = self._get_all_cities()

        for city in raw_cities:
            if city['province'].endswith('市'):
                cities.append(city['province'].rstrip('市'))
            elif '直辖县级行政区划' in city['name']:
                continue
            else:
                cities.append(city['name'].rstrip('市'))

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

    def save_subscription(uid, city):
        '''保存一个用户对于制定城市的订阅'''
        pass

    def cancel_subscription(uid, city):
        '''取消一个用户对于指定城市的订阅'''
        pass

    def get_subscribed_users(city):
        '''获取所有订阅指定城市的用户'''
        pass
