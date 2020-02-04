##### 此文件已被弃用，只是留作参考用 #####


import os
import time
import random
import json

import requests
import pandas as pd

from .constants import *
from ..utils.log import Logger


logger = Logger('upload_latest_json')


def load_response():
    try:
        api = 'https://service-f9fjwngp-1252021671.bj.apigw.tencentcs.com/release/pneumonia'
        response = requests.get(api, headers=REQUEST_HEADERS).json()
        if not response['data']['listByArea']:
            raise Exception(response)
        ls.logging.info('json loaded at time {}'.format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        return response
    except Exception as e:
        logger.error('json load failed, waiting for around 15 seconds')
        logger.exception(e)
        time.sleep(15 + 5 * random.random())
        return load_response()


def load_json(file_name='assets/data/latest.json'):
    with open(file_name, 'r+') as f:
        return json.load(f)


def write_json(file_name, js):
    with open(file_name, 'w+') as f:
        json.dump(js, f)


def p():
    print(0)


class Data(object):
    def __init__(self, *on_updates):
        self.response = None
        self.provinces = []
        self.time_stamp = 0
        self.suspect = 0
        self.confirmed = 0
        self.cured = 0
        self.dead = 0
        self.data_dict = {}
        self.diff_dict = {}
        self.on_updates = on_updates
        self.update()

    def load_stat(self, area_stat):
        return [Province(province_stat) for province_stat in area_stat]

    def init(self):
        try:
            latest_response = load_response()
            if self.response and latest_response['data']['listByArea'] == self.response['data']['listByArea']:
                return False
            else:
                old_dict = self.data_dict
                self.response = latest_response
                self.provinces = self.load_stat(
                    self.response['data']['listByArea'])
                self.time_stamp = time.time()
                self.suspect = 0
                self.confirmed = 0
                self.cured = 0
                self.dead = 0
                self.data_dict = {}
                for province in self.provinces:
                    self.suspect += province.suspect
                    self.confirmed += province.confirmed
                    self.cured += province.cured
                    self.dead += province.dead
                    self.data_dict[province.name] = \
                        [province.suspect, province.confirmed,
                            province.cured, province.dead]
                    for city in province.cities:
                        self.data_dict[city.name] = [
                            city.suspect, city.confirmed, city.cured, city.dead]
                self.diff_dict = {k: v for k, v in self.data_dict.items(
                ) if k not in old_dict or old_dict[k] != v}
                ls.logging.info('data constructed')
                return True
        except Exception as e:
            ls.logging.error('data construction failed')
            ls.logging.exception(e)
            time.sleep(15 + 10 * random.random())
            self.init()

    def update(self):
        ret = self.init()
        if ret:
            ls.logging.info('data updated at {}'.format(self.time_stamp))
            self.on_update()

    def on_update(self):
        # write_json('./jsons/{}.json'.format(self.time_stamp), self.response)
        write_json('./jsons/latest.json', self.response)
        for func in self.on_updates:
            try:
                func()
            except Exception as e:
                ls.logging.error('calling {} failed'.format(func))
                ls.logging.exception(e)


class Province(object):
    def __init__(self, province_stat):
        self.name = province_stat['provinceName']
        self.abbreviation = province_stat['provinceShortName']
        self.suspect = province_stat['suspected']
        self.confirmed = province_stat['confirmed']
        self.cured = province_stat['cured']
        self.dead = province_stat['dead']
        self.cities = self.load_stat(province_stat['cities'])
        self.comment = province_stat['comment']

    def load_stat(self, province_stat_cities):
        return [City(city_stat) for city_stat in province_stat_cities]


class City(object):
    def __init__(self, city_stat):
        self.name = city_stat['cityName']
        self.suspect = city_stat['suspected']
        self.confirmed = city_stat['confirmed']
        self.cured = city_stat['cured']
        self.dead = city_stat['dead']


def update_latest_data():
    data = Data(p)
    while True:
        time.sleep(100)
        response = load_response()
        if response['data']['listByArea'] != data.response['data']['listByArea']:
            data.update()


if __name__ == "main":
    update_latest_data()
