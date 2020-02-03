import json
import datetime

from werobot.client import Client

from ..config import DATABASE, DATA_DIR, UPDATES_FILENAME
from ..utils.log import Logger
from ..utils.db_connect import RedisConnect, SQLiteConnect
from ..spider.spider_utils import get_should_update, remove_update


updates_file = DATA_DIR / UPDATES_FILENAME


class PushUpdatesClient:
    '''推送数据更新封装类'''

    def __init__(self, app_id, app_secret):
        self.logger = Logger('push')

        config = {'APP_ID': app_id, 'APP_SECRET': app_secret}
        self.client = Client(config)

        if DATABASE == 'redis':
            self.db = RedisConnect()
        elif DATABASE == 'sqlite':
            self.db = SQLiteConnect()

    # def add_custom_service_account(self, account, nickname, password):
    #     self.client.add_custom_service_account(account, nickname, password)

    # def send_text_message(self, user_id, content):
    #     self.client.send_text_message(user_id, content)

    def send_template_message(self, user_id, template_id, data, url=''):
        self.client.send_template_message(user_id, template_id, data, url)
    
    def parse_update_into_message(self, area):

    def main(self):
        # 检查是否有需要推送的数据更新
        if not get_should_update():
            return
        with updates_file.open() as f:
            updates = json.load(f)

        # TODO: 最好把所有一个用户所有的订阅更新在一条消息里推送？
        for area in updates:
            subscribed_users = self.db.get_subscribed_users(area['area'])
            if not subscribed_users:
                continue

            template_data = {
                'data': {
                    'value': '新增死亡：{}'.format(area['n_dead']),
                    'color': '#aa3177'
                },
                'date': {
                    'value': datetime.datetime.now().strftime('%Y%m%d %H:%M:%S'),
                    'color': '#17aa77'
                },
                'city': {
                    'value': area['parent'] + area['area'],
                    'color': '#1731aa'
                }
            }
            for user in subscribed_users:
                self.send_template_message(user, TEMPLATE_ID, template_data)
        
        # 完成推送，删除数据更新文件
        remove_update()
