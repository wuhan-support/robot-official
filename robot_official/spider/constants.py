from pathlib import Path


DATA_URL = 'https://view.inews.qq.com/g2/getOnsInfo'
REGION_PARAM = {'name': 'disease_h5'}
NATIONAL_PARAM = {'name': 'wuwei_ww_global_vars'}

REQUEST_HEADERS = {
    'host': 'view.inews.qq.com',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'referer': 'https://news.qq.com/zt2020/page/feiyan.htm'
}

SPLIT_ABBR_SUFFIX = r'(.*?)((?:自治[区州])|省|市|县|(?:新?区)|镇)'
