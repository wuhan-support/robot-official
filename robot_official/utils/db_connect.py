import redis
import sqlalchemy as sql

from .log import Logger
from ..config import SQLITE_FILE, REDIS_HOST, REDIS_PORT


logger = Logger('db')


class SQLiteConnect:
    '''SQLite 数据库接口封装类'''

    def __init__(self, db_file=SQLITE_FILE):
        # 目前机器人线程、爬虫线程和推送线程都会访问同一个SQLite数据库
        # 这个操作会引起SQLite多线程错误警告
        # 我暂时性使用了忽略警告的办法，但是这不是一个优雅的甚至不是好的解决方法
        # 未来需要更好的解决方法
        # TODO: Make this class into a singleton
        self.engine = sql.create_engine('sqlite:///{}'.format(db_file), connect_args={'check_same_thread': False})
        self.conn = self.engine.connect()
        self.metadata = sql.MetaData()
        self.areas_list = []

        self._initialize_tables()

    def _initialize_tables(self):
        '''初始化数据库表'''
        self.areas = sql.Table('areas', self.metadata,
            sql.Column('id', sql.Integer(), primary_key=True, nullable=False),
            sql.Column('name', sql.String(255)),
            sql.Column('abbr', sql.String(255)),
            sql.Column('suffix', sql.String(16)),
            sql.Column('parent', sql.String(255)),
        )

        self.subscriptions = sql.Table('subscriptions', self.metadata,
            sql.Column('id', sql.Integer(), primary_key=True, nullable=False),
            sql.Column('uid', sql.String(255), nullable=False),
            sql.Column('area_id', sql.Integer(), sql.ForeignKey('areas.id'), nullable=False),
        )

        self.metadata.create_all(self.engine)
        logger.info('数据库表初始化完成')
 
    def get_all_areas(self):
        '''返回目前数据库中所有的地区名称'''
        query = sql.select([self.areas.c.name])
        result_proxy = self.conn.execute(query)
        results = result_proxy.fetchall()

        return [area.name for area in results]

    def save_area(self, abbr, suffix, parent):
        '''保存一个地区至数据库'''
        # TODO: 检查是否地区已经存在
        query = self.areas.insert().values(abbr=abbr, suffix=suffix, name=abbr + suffix, parent=parent)
        self.conn.execute(query)
    
    def _match_target_to_areas(self, target) -> list:
        '''返回数据库中所有匹配关键词的地区对象'''
        # TODO: 可能可以添加模糊搜索
        # TODO: 使用缓存（或许Redis?）
        query = sql.select([self.areas]).where(
            sql.or_(
                self.areas.c.abbr == target,
                self.areas.c.name == target
            )
        )
        result_proxy = self.conn.execute(query)
        results = result_proxy.fetchall()
        if len(results) < 1:
            # 未找到地区名
            return []
        return results

    def save_subscription(self, uid, target):
        '''保存一个用户对于指定地区的订阅，并返回返回码及地区显示名称'''
        areas = self._match_target_to_areas(target)
        if not areas:
            return -1, ''
        elif len(areas) > 1:
            area = areas[0] # TODO: 处理多个匹配
        else:
            area = areas[0]
        area_display_name = get_area_display_name(area)

        # 插入数据
        # TODO: 检查是否已经存在该订阅
        query = self.subscriptions.insert().values(uid=uid, area_id=area.id)
        self.conn.execute(query)

        return 0, area_display_name

    def cancel_subscription(self, uid, target):
        '''取消一个用户对于指定地区的订阅，并返回返回码及地区显示名称'''
        areas = self._match_target_to_areas(target)
        if not areas:
            return -1, ''
        elif len(areas) > 1:
            areas = [areas[0]] # TODO: 处理多个匹配
        area = areas[0]
        area_display_name = get_area_display_name(area)

        # 删除数据
        try:
            query = sql.delete(self.subscriptions).where(
                sql.and_(
                    self.subscriptions.c.uid == uid,
                    self.subscriptions.c.area_id == area.id
                )
            )
            self.conn.execute(query)
        except Exception:
            # 为了不query两遍，我采用捕获异常的方法来判断订阅是否存在
            return -1, ''

        return 0, area_display_name

    def get_subscribed_users(self, target):
        '''获取所有订阅指定地区的用户，返回UID列表'''
        areas = self._match_target_to_areas(target)
        if not areas:
            return []
        elif len(areas) > 1:
            areas = [areas[0]] # TODO: 处理多个匹配
        area = areas[0]
        
        query = sql.select([self.subscriptions]).where(self.subscriptions.c.area_id == area.id)
        result_proxy = self.conn.execute(query)
        results = result_proxy.fetchall()

        return [sub.uid for sub in results]


class RedisConnect:
    '''Redis 数据库接口封装类'''

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=None):
        self.r = redis.Redis(host=host, port=port, decode_responses=True, password=password)
        logger.info('数据库表初始化完成')

    def get_all_areas(self):
        '''返回目前数据库中所有的地区名称'''
        return self.r.smembers('all_areas')

    def save_area(self, abbr, suffix, parent):
        '''保存一个地区至数据库'''
        name = abbr + suffix
        self.r.sadd('all_areas', name)
        self.r.sadd('all_areas', abbr) # TODO: 为了查找用，但会导致重名地区数据覆盖，需修复
        self.r.hmset('area:{}'.format(name), {
            'abbr': abbr,
            'suffix': suffix,
            'name': name,
            'parent': parent
        })

    def _match_target_to_area(self, target) -> list:
        '''返回数据库中匹配关键词的地区对象'''
        # TODO: 处理重名情况
        return self.r.hgetall('area:{}'.format(target))

    def save_subscription(self, uid, target):
        '''保存一个用户对于指定地区的订阅，并返回返回码及地区显示名称'''
        area = self._match_target_to_area(target)
        if not area:
            return -1, ''
        area_display_name = get_area_display_name(area)
        self.r.sadd('sub:{}'.format(area['name']), uid)

        return 0, area_display_name

    def cancel_subscription(self, uid, target):
        '''取消一个用户对于指定地区的订阅，并返回返回码及地区显示名称'''
        area = self._match_target_to_area(target)
        if not area:
            return -1, ''
        area_display_name = get_area_display_name(area)
        self.r.srem('sub:{}'.format(area['name']), uid)

        return 0, area_display_name
    
    def get_subscribed_users(self, target):
        '''获取所有订阅指定地区的用户，返回UID列表'''
        area = self._match_target_to_area(target)
        if not area:
            return []
        return self.r.smembers('sub:{}'.format(area['name']))


def get_area_display_name(area):
    '''返回一个用户友好的地区名称，包含其父地区（除非是中国）'''
    # 两种不同的area会被传入，需要分开处理
    try:
        parent = area.get('parent', '')
        name = area.get('name', '')
    except Exception as e:
        logger.warning('无法获取地区用户友好名称：{}'.format(area))
        logger.exception(e)
        return ''
    area_display_name = '' if parent in ('全国', '中国') else parent
    area_display_name += name
    return area_display_name
