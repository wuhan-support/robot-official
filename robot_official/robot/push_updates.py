import json
import datetime

from werobot.client import Client

from ..config import APP_ID, APP_SECRET, TEMPLATE_ID, DATABASE, DATA_DIR, UPDATES_FILENAME
from ..utils.log import Logger
from ..utils.db_connect import RedisConnect, SQLiteConnect
from ..spider.spider_utils import get_should_update, remove_update


updates_file = DATA_DIR / UPDATES_FILENAME


class PushUpdatesClient:
    '''推送数据更新封装类'''

    def __init__(self, app_id=APP_ID, app_secret=APP_SECRET):
        self.logger = Logger('PushClient')

        client_config = {'APP_ID': app_id, 'APP_SECRET': app_secret}
        self.client = Client(client_config)

        if DATABASE == 'redis':
            self.db = RedisConnect()
        elif DATABASE == 'sqlite':
            self.db = SQLiteConnect()

    def parse_update_into_message(self, area):
        msg = '新增'
        msg += '确诊 {} 例'.format(area['n_confirm']) if area['n_confirm'] != 0 else ''
        msg += '疑似 {} 例'.format(area['n_suspect']) if area['n_suspect'] != 0 else ''
        msg += '死亡 {} 例'.format(area['n_dead']) if area['n_dead'] != 0 else ''
        msg += '治愈 {} 例'.format(area['n_heal']) if area['n_heal'] != 0 else ''
        msg += '\n'
        msg += '截至目前总计'
        msg += '确诊 {} 例'.format(area['confirm'])
        msg += '死亡 {} 例'.format(area['dead'])
        msg += '治愈 {} 例'.format(area['heal'])
        return '\n{}\n'.format(msg)

    def main(self):
        # 检查是否有需要推送的数据更新
        if not get_should_update():
            self.logger.debug('无数据更新，无需推送')
            return
        with updates_file.open() as f:
            updates = json.load(f)
            self.logger.info('准备推送共{}个地区的数据更新'.format(len(updates)))

        # TODO: 最好把所有一个用户所有的订阅更新在一条消息里推送？
        for area in updates:
            subscribed_users = self.db.get_subscribed_users(area['area'])
            if not subscribed_users:
                continue

            template_data = {
                'area': {
                    'value': self.db.get_area_display_name(area),
                    'color': '#2980b9'
                },
                'update': {
                    'value': self.parse_update_into_message(area),
                    'color': '#d35400'
                },
                'datetime': {
                    'value': datetime.datetime.now().strftime('%Y年%-m月%-d日 %H:%M'),
                    'color': '#7f8c8d'
                }
            }
            for user in subscribed_users:
                self.client.send_template_message(user, TEMPLATE_ID, template_data)
        
        # 完成推送，删除数据更新文件
        remove_update()
        self.logger.info('全部更新推送完成')
