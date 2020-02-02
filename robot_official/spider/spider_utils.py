import json

from .constants import DATA_DIR, DATA_FILE_ALL, UPDATE_FLAG_FILE


def load_stored_data() -> dict:
    '''读取存储的数据'''
    data_file = DATA_DIR / DATA_FILE_ALL
    if not data_file.exists():
        return {}
    with data_file.open() as f:
        return json.load(f)


def store_data(data: dict):
    '''存储数据至JSON文件'''
    save_file = DATA_DIR / DATA_FILE_ALL
    with save_file.open('w') as f:
        return json.dump(data, f)


def get_should_update():
    '''返回是否有数据更新'''
    return UPDATE_FLAG_FILE.exists()


def set_should_update(state):
    '''更改是否有数据更新'''
    if state:
        UPDATE_FLAG_FILE.open('w')
    else:
        UPDATE_FLAG_FILE.unlink(missing_ok=True)
