import json

from ..config import DATA_DIR, DATA_ALL_FILENAME, UPDATES_FILENAME


all_data_file = DATA_DIR / DATA_ALL_FILENAME
updates_file = DATA_DIR / UPDATES_FILENAME


def load_stored_data() -> dict:
    '''读取存储的数据'''
    if not all_data_file.exists():
        return {}
    with all_data_file.open() as f:
        return json.load(f)

def store_data(data: dict):
    '''存储数据至JSON文件'''
    with all_data_file.open('w') as f:
        return json.dump(data, f)


def get_should_update():
    '''返回是否有数据更新'''
    return updates_file.exists()

def remove_update():
    '''删除存储的地区数据更新'''
    try:
        updates_file.unlink()
    except FileNotFoundError:
        # Python 3.6 暂不支持 missing_ok
        pass

def set_update(data):
    '''存储有更新的地区数据'''
    with updates_file.open('w') as f:
        json.dump(data, f)
