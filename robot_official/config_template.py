from pathlib import Path

# 微信公众号/服务号 token
TOKEN = 'YOUR_TOKEN'
TEMPLATE_ID = 'YOUR_TEMPLATE_ID'

# 微信公众号/服务号 AppID 及 AppSecret
APP_ID = 'YOUR_APP_ID'
APP_SECRET = 'YOUR_APP_SECRET'

# 机器人监听
ROBOT_HOST = 'auto' # 默认: 'auto'
ROBOT_PORT = 8000 # 默认: 8000

# 数据库选择
DATABASE = 'sqlite' # 目前只支持 sqlite 或 redis

# Redis 服务器
REDIS_HOST = 'localhost' # 默认: 'localhost'
REDIS_PORT = 6379 # 默认: 6379

# SQLite 配置
SQLITE_FILE = 'feiyan-help.sqlite' # 默认: 'feiyan-help.sqlite'

# 数据存储
DATA_DIR = Path('assets/data/')
DATA_ALL_FILENAME = 'latest.json' # 存储所有数据的文件名
UPDATES_FILENAME = 'updates.json' # 存储任何待推送的更新的文件名

# 更新间隔
UPDATE_INTERVAL = 60 * 5 # 秒
