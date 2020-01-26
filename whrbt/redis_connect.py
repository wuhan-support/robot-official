import redis
class Connect:
    def __init__(self,host="localhost",port=6379):
        self.host=host
        self.port=port
        self.r=self._connect(self.host,self.port)
    def _connect(self,host,port):
        return redis.Redis(host=host,port=port)
    def addUser(self,wechat_id,city):
        self.r.sadd(wechat_id,city)
    def deleteUser(self,wechat_id,city):
        self.r.