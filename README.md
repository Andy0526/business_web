一个基于 python 的 flask 框架的资讯网站

演示地址： http://119.29.100.53:8086/
----

# 1 背景介绍
该比赛要求参赛者开发一款数据舆情产品，帮助用户了解 P2P 行业现状。本人在比赛中负责网站的设计、开发和部署。团队最终排名第2。涉及内容：
* 前端：HTML5 + CSS + JavaScript+JSON<br>
* 后台：Python轻量级Web应用框架Flask<br>

# 2 项目基本介绍
* [项目介绍PPT](https://github.com/mindawei/p2p/blob/master/doc/klj.pdf)。
* 本项目主要是一个展示数据的网站。
* 数据来源是其它三位队友爬取数据后处理得到的，他们的项目在[ others ](https://github.com/mindawei/p2p/tree/master/others)目录中。
* 本项目数据源在[ static/data ](https://github.com/mindawei/p2p/tree/master/static/data)目录中，项目启动前需要将它们导入到 mongodb 数据库中。

# 3 QuickStart
## 3.1 安装环境
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

## 3.2 启动项目
1. 在 mongodb 目录的 bin 目录中执行 mongod.exe 文件。<br>
`C:\software\mongdb3.6.3\bin>mongod --dbpath C:\software\mongdb3.6.3\db`
![](https://github.com/mindawei/p2p/blob/master/doc/imgs/01.png)

2. 将数据导入到 mongodb 数据库中。<br>
项目目录下运行 `data_to_mongodb.py` 文件， 命令行输入 `python data_to_mongodb.py`。
![](https://github.com/mindawei/p2p/blob/master/doc/imgs/02.png)

3. 启动项目。<br>
项目目录下运行 `run.py` 文件, 命令行输入 `python run.py`。
![](https://github.com/mindawei/p2p/blob/master/doc/imgs/03.png)

4. 访问项目<br>
输入 `http://localhost:8086` 进行访问。

# 4 效果展示
访问地址： http://119.29.100.53:8086/

一个测试账号 用户名：test  密码： 123

![](https://github.com/mindawei/p2p/blob/master/doc/imgs/04.png)

![](https://github.com/mindawei/p2p/blob/master/doc/imgs/05.png)

![](https://github.com/mindawei/p2p/blob/master/doc/imgs/06.png)

![](https://github.com/mindawei/p2p/blob/master/doc/imgs/07.png)

![](https://github.com/mindawei/p2p/blob/master/doc/imgs/08.png)

![](https://github.com/mindawei/p2p/blob/master/doc/imgs/09.png)

# 5 后续项目
[zsw](https://github.com/mindawei/zsw) 是基于该项目的一个简化版本，但是增加了一些帖子评论等功能。

