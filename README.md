# 微信公众号 / 个人微信机器人

该项目还在进行中并且需要您的帮助，我们希望能让所有人都变成自媒体，您若赋闲在家，不妨搭建自己小型的机器人，传播消息更传播爱。

### 基本用法
更新疫情信息
> python load_json.py

推送模板消息
> python sv_account.py

连接服务号并接收回调信息
> python app.py
### 数据库
计划使用redis和sqlite
### 具体使用
搜索微信公众号测试版，申请账号，并配置

config.py中填入TEMPLATE_ID，APP_ID,SECRET_ID

个人微信号机器人很快上线
### 计划
- [x] 与疫情数据接入（dataset仓库）
- [ ] 与其他信息接入（人工收集）  

