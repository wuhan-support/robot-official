from werobot import WeRoBot

from .config import ROBOT_HOST, ROBOT_PORT, APP_ID, APP_SECRET, TOKEN, ENCODING_AES_KEY, DATABASE
from .utils.log import Logger
from .utils.db_connect import RedisConnect, SQLiteConnect
from .utils.robot_msg import is_subscribe_msg, is_unsubscribe_msg


logger = Logger('robot')

app_config = {
    'HOST': ROBOT_HOST,
    'PORT': ROBOT_PORT,
    'APP_ID': APP_ID,
    'APP_SECRET': APP_SECRET,
    'TOKEN': TOKEN,
    'ENCODING_AES_KEY': ENCODING_AES_KEY
}
app = WeRoBot(config=app_config, logger=logger)
logger.info('初始化 WeRoBot 完成')

logger.info('数据库类型: {}'.format(DATABASE))
if DATABASE == 'redis':
    db = RedisConnect()
elif DATABASE == 'sqlite':
    db = SQLiteConnect()
else:
    logger.critical('未知数据库类型，无法初始化')
    exit()
logger.info('数据库初始化完成')


# 文字消息处理句柄
@app.text
def reply_text(message):
    wechat_id = message.source
    msg = message.content

    # 这里存储订阅还可以使用微信官方提供的标签系统来实现
    # 但使用数据库无疑是对公众号影响最小的实现方法

    is_subscribe, target = is_subscribe_msg(msg)
    if is_subscribe:
        if not target:
            return '请输入地区名称（如：订阅武汉）。'

        code, sub_area_name = db.save_subscription(wechat_id, target)
        if code != -1:
            return '成功订阅{}的疫情信息！'.format(sub_area_name)
        else:
            return '尝试订阅{}失败，该地区名称不正确或暂无疫情信息。'.format(target)

    is_unsubscribe, target = is_unsubscribe_msg(msg)
    if is_unsubscribe:
        if not target:
            return '请输入地区名称（如：取消订阅武汉）。'
        
        code, sub_area_name = db.save_subscription(wechat_id, target)
        elif code != -1:
            return '成功取消{}的疫情信息订阅。'.format(sub_area_name)
        else:
            return '尝试取消{}的疫情信息订阅失败，您好像没有订阅该地区信息或者地区名称错误。'.format(target)

    return '输入有误，请重新输入'


# 订阅消息处理句柄
@app.subscribe
def account_subscribe(message):
    return '感谢关注'
