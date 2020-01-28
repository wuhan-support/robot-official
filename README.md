# 微信公众号 / 个人微信机器人

### 个人微信号机器人
个人微信号机器人已经上线，[友情链接](https://github.com/wuhan-support/NcovWeRobotPersonal)

### 目的
该项目还在进行中并且需要您的帮助，我们希望能让所有人都变成自媒体，您若赋闲在家，不妨搭建自己小型的机器人，传播消息更传播爱。


### 基本用法

推送模板消息，同时更新疫情数据
> python sv_account.py

连接服务号并接收回调信息，需要自己更改配置
> python app.py

### 数据库
计划使用 Redis 以及 SQLite


### 具体使用
搜索微信公众号测试版，申请账号，并配置

`config.py` 中填入 `TEMPLATE_ID`, `APP_ID`, `SECRET_ID`

![图片1](./whrbt/image/dd060b73dd42a283f38fd3b5dec61c6.jpg)
![图片2](./whrbt/image/d993601c9252ef548d8dbffbd724266.jpg )

支持各省市，全国，输入暂时需要缩写，不带“省”，“市”

### 计划
- [x] 与疫情数据接入
- [ ] 其他信息（人工收集，[详情参考](http://feiyan.help)） 
- [ ] 其他信息（爬虫收集）

