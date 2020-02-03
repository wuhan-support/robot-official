import os
import re
import json
from urllib import parse

import requests

# from src.util.constant import ALL_AREA_KEY, AREA_TAIL, SHOULD_UPDATE, STATE_NCOV_INFO, UPDATE_CITY, TIME_SPLIT, \
#     USE_REDIS, BASE_DIR, DATA_DIR
# from src.util.redis_config import connect_redis, save_json_info, load_last_info, save_json_info_as_key
# from src.util.sqlite_config import SQLiteConnect
# from src.util.util import check_dir_exist

from .constants import *
from .spider_utils import *
from ..config import *
from ..utils.log import Logger
from ..utils.db_connect import RedisConnect, SQLiteConnect


class TXSpider():
    '''腾讯新闻平台的实时疫情数据爬虫'''

    def __init__(self):
        self.logger = Logger('TXSpider')
        self.req = requests.Session()
        if DATABASE == 'redis':
            self.db = RedisConnect()
        elif DATABASE == 'sqlite':
            self.db = SQLiteConnect()
        
        DATA_DIR.mkdir(exist_ok=True)

    # def check_dirs(self):
    #     check_dir_exist(DATA_DIR)
    #     check_dir_exist(os.path.join(os.path.join(BASE_DIR, "download_image")))

    def main(self):
        try:
            self.logger.info('开始爬取疫情数据')
            raw_data = self.get_raw_realtime_data()
            latest_data = self.process_raw_data(raw_data['areaTree'])
            # 腾讯 areaTree 中的全国数据与 chinaTotal 不一致，以 chinaTotal 为准
            latest_data['全国'].update(raw_data['chinaTotal'])
            # chinaTotal = data['chinaTotal']
            # latest_data['全国']['confirm'] = int(chinaTotal['confirm'])
            # latest_data['全国']['suspect'] = int(chinaTotal['suspect'])
            # latest_data['全国']['dead'] = int(chinaTotal['dead'])
            # latest_data['全国']['heal'] = int(chinaTotal['heal'])

            # 计算该数据与上一次数据之差
            previous_data = load_stored_data()
            updated_areas = self.parse_data_change(previous_data, latest_data)
            self.logger.debug('共有{}个地区存在数据更新'.format(len(updated_areas)))

            # 保存所有地区名称至数据库及JSON
            self.save_all_areas(latest_data) # 数据库
            store_data(latest_data) # JSON

            # 如果数据有更新，则保存新数据和更新的数据
            if len(updated_areas) > 0:
                store_data(updated_areas) # 存储最新数据至JSON
                if get_should_update():
                    # TODO: 如果上一次的数据更新还未推送，要合并新增数据
                    # old_update_city = self.get_old_data_city()
                    # if old_update_city != None:
                    #     updated_areas = self.merge_update_city(old_city_list=old_update_city, new_city_list=updated_areas)
                    pass
                else:
                    set_update(updated_areas)
                self.logger.info('更新了{}个地区的疫情数据'.format(len(updated_areas)))
                updated_names = '、'.join([area['area'] for area in updated_areas])
                self.logger.debug('更新了以下地区的数据：{}'.format(updated_names))
            else:
                # self.re.set(SHOULD_UPDATE, 0)
                self.logger.info('没有地区有疫情数据更新')

        except Exception as e:
            self.logger.exception(e)

    def get_old_data_city(self):
        try:
            if USE_REDIS:
                old_update_city = json.loads(self.re.get(UPDATE_CITY))
            else:
                file = os.path.join(DATA_DIR, UPDATE_CITY + ".json")
                with open(file, 'r', encoding='utf-8') as r:
                    old_update_city = json.load(r)
            return old_update_city
        except Exception as e:
            self.logger.error("Error: failed to load old update city")
            self.logger.exception(e)
            return None

    def merge_update_city(self, new_city_list, old_city_list):
        final_result = []
        old_city = {x['city']: x for x in old_city_list}
        new_city = {x['city']: x for x in new_city_list}

        for city in new_city_list:
            if city['city'] in old_city:
                city['n_confirm'] += old_city[city['city']]['n_confirm']
                city['n_suspect'] += old_city[city['city']]['n_suspect']
                city['n_dead'] += old_city[city['city']]['n_dead']
                city['n_heal'] += old_city[city['city']]['n_heal']
                final_result.append(city)
            else:
                final_result.append(city)

        for city in old_city_list:
            if city['city'] not in new_city:
                final_result.append(city)
        return final_result

    # def get_state_all(self):
    #     """
    #     获取全国数据
    #     :return:
    #     """
    #     res = self.req.get(url=DATA_URL, params=REGION_PARAM, headers=REQUEST_HEADERS)
    #     if res.status_code != 200:
    #         self.logger.error("获取全国数据失败")
    #     data = json.loads(json.loads(res.content.decode("utf-8"))['data'])[0]
    #     state_dict = {}
    #     state_dict['confirm'] = data['confirmCount']
    #     state_dict['dead'] = data['deadCount']
    #     state_dict['heal'] = data['cure']
    #     state_dict['suspect'] = data['suspectCount']
    #     state_dict['area'] = '全国'
    #     state_dict['country'] = '全国'
    #     state_dict['city'] = '全国'
    #     return {'全国': state_dict}

    def get_raw_realtime_data(self):
        '''从腾讯新闻获取各地疫情的原始实时数据'''
        res = self.req.get(url=DATA_URL, params=REGION_PARAM, headers=REQUEST_HEADERS)
        if res.status_code != 200:
            self.logger.error('尝试获取地区数据失败 ({})'.format(res.status_code))
            raise ConnectionError
        data = json.loads(res.json()['data'])
        return data

    def process_raw_data(self, data, parent=''):
        '''处理爬取到的原始数据，并返回一个字典'''
        data_dict = {}
        for area in data:
            if area['name'] == '待确认':
                continue
            elif area['name'] == '朝阳':
                # 区分辽宁省朝阳市和北京市朝阳区
                area['name'] = '朝阳区'
            elif area['name'] == '中国':
                area['name'] ='全国'
            area_key = area['name']

            # 保存该地区数据
            area_data = area['total']
            area_data.update({
                'city': area['name'], # 这是干嘛的？
                'area': area['name'],
                'parent': parent,
                # 'today_confirm': area['today']['confirm'],
                # 'today_suspect': area['today']['suspect'],
                # 'today_dead': area['today']['dead'],
                # 'today_heal': area['today']['heal']
            })
            data_dict[area_key] = area_data
            if 'children' in area:
                # 对地区的子地区进行递归处理
                data_dict.update(self.process_raw_data(area['children'], area_key))
        return data_dict

    # def fill_unknow(self, data):
    #     for item in data:
    #         if 'city' not in item or item['city'] == '':
    #             if 'area' not in item or item['area'] == '':
    #                 item['city'] = item['country']
    #                 item['area'] = item['country']
    #             else:
    #                 item['city'] = item['area']
    #     return data

    def save_all_areas(self, data_dict):
        '''保存所有地区的名称，供分词用'''
        all_area = set(data_dict.keys())
        saved_areas = set(self.db.get_all_areas())
        new_areas = all_area - saved_areas

        for area in new_areas:
            match = re.match(SPLIT_ABBR_SUFFIX, area)
            if not match:
                abbr = area
                suffix = ''
            else:
                abbr, suffix = match.groups()
            if len(abbr) < 2:
                # 不存在单字的地区名称
                continue
            parent = data_dict[area]['parent']
            self.db.save_area(abbr, suffix, parent)

    def parse_data_change(self, previous_data, new_data):
        '''计算有更新的地区'''
        previous_data = {previous['area']: previous for previous in previous_data} # 统一数据格式
        updated_areas = []
        for key, area in new_data.items():
            previous = previous_data.get(key)
            if previous:
                new_data[key]['n_confirm'] = area['confirm'] - previous['confirm']
                new_data[key]['n_suspect'] = area['suspect'] - previous['suspect']
                new_data[key]['n_dead'] = area['dead'] - previous['dead']
                new_data[key]['n_heal'] = area['heal'] - previous['heal']
            else:
                new_data[key]['n_confirm'] = area['confirm']
                new_data[key]['n_suspect'] = area['suspect']
                new_data[key]['n_dead'] = area['dead']
                new_data[key]['n_heal'] = area['heal']
            if self.check_whether_update(new_data[key]):
                updated_areas.append(new_data[key])
        return updated_areas

    def check_whether_update(self, area):
        '''检查是否有数据更新（新旧数据之差是否大于0）'''
        return sum((area['n_confirm'], area['n_suspect'], area['n_dead'], area['n_heal'])) > 0


if __name__=='__main__':
    spider = TXSpider()
    spider.main()
