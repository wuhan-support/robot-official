# -*-coding:utf-8-*-
from werobot import WeRoBot
import re

from .redis_connect import Connect

client=Connect(host="localhost",port=6379)

class customService:
    """
    客服服务，回复消息，根据city获取用户id，并发送
    """
    pass
class redisToMysql:
    """
    将redis的内容每过一段时间更新进mysql
    """
    pass

@robot.text
def echo(message):
    wechat_id=message.source
    sub_city = re.compile("sub(.*)")
    pop_city=re.compile("pop(.*)")
    if sub_city:
        client.addUser(sub_city,wechat_id)
        return "订阅成功"
    if pop_city:
        client.deleteUser(pop_city,wechat_id)
        return "删除成功"
    return ""



@robot.subscribe
def account_subcribe():
    return """
    subscribe!
    """



if __name__=="main":
    
    robot = WeRoBot(token="ye980226")
    robot.run("auto", port=8000)
