拍拍贷魔镜杯数据产品大赛（银奖）：一个P2P资讯的网站
----

# 1背景介绍
该比赛要求参赛者开发一款数据舆情产品，帮助用户了解 P2P 行业现状。本人在比赛中负责网站的设计、开发和部署。最终排名第2，获得银奖和5万元奖金。

涉及内容：
* 前端：HTML5 + CSS + JavaScript+JSON<br>
* 后台：Python轻量级Web应用框架Flask<br>

# 2 QuickStart
## 2.1 安装环境
1. 安装 python 2.7<br>
下载 python 安装文件，安装后配置系统环境变量。<br>
可参考[《Flask入门_Windows下安装》](https://www.cnblogs.com/Christeen/p/6514713.html)

2. 安装 flask<br>
命令行运行 `pip install flask`。<br>
可参考[《Flask入门_Windows下安装》](https://www.cnblogs.com/Christeen/p/6514713.html)

3. 安装 pymongo<br>
命令行运行 `pip install pymongo`。

4. 安装mongodb 数据库<br>
* 官网下载[安装包](https://www.mongodb.com/download-center#community)
* 创建一个db文件夹，我的文件位置是 `C:\software\mongdb3.6.3\db`
可参考[《Windows 平台安装 MongoDB》](http://www.runoob.com/mongodb/mongodb-window-install.html)

## 2.2 启动项目
1. 在 mongodb 目录的 bin 目录中执行 mongod.exe 文件。<br>
`C:\software\mongdb3.6.3\bin>mongod --dbpath C:\software\mongdb3.6.3\db`

2. 将数据导入到 mongodb 数据库中。<br>
项目目录下运行 `data_to_mongodb.py` 文件， 命令行输入 `python data_to_mongodb.py`。

3. 启动项目。<br>
项目目录下运行 `run.py` 文件, 命令行输入 `python run.py`。

4. 访问项目<br>
输入 `http://localhost:8086` 进行访问。

# 3 效果展示
访问地址： http://119.29.100.53:8086/

一个测试账号 用户名：test  密码： 123
