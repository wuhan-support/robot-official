# -*-coding:utf-8-*-
from werobot import WeRoBot
import re
from werobot.client import Client as InformationClient #消息类
from redis_connect import Connect

r=Connect(host="localhost",port=6379)
APP_ID=""
APP_SECRET=""
class customService:
    """
    客服服务，回复消息，根据city获取用户id，并发送
    """
    def __init__(self,APP_ID,APP_SECRET):
        config={"APP_ID":APP_ID,"APP_SECRET":APP_SECRET}
        self.client=InformationClient(config)
    def addCustomServiceAccount(self,account,nickname,password):
        self.client.add_custom_service_account(account,nickname,password)
    def sendTextMessage(self,user_id,content):
        self.client.send_text_message(user_id,content)
    
    
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
        r.addUser(sub_city,wechat_id)
        return "订阅成功"
    if pop_city:
        r.deleteUser(pop_city,wechat_id)
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
