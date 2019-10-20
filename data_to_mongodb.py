# -*- coding: utf-8 -*-

import json
import csv

from pymongo import MongoClient

# 连接
conn = MongoClient('localhost', 27017)
# 连接数据库
db = conn.p2p

# 资讯类型

# 新闻入库
db.news.remove()
data = json.load(open('static/data/raw/news.json', 'r'))
db.news.insert(data)
print("now the number of news is:%d" % db.news.count())

# 政策入库
db.policy.remove()
data = json.load(open('static/data/raw/policy.json', 'r'))
db.policy.insert(data)
print("now the number of policy is:%d" % db.policy.count())

# 政策入库
db.opinion.remove()
data = json.load(open('static/data/raw/opinion.json', 'r'))
db.opinion.insert(data)
print("now the number of opinion is:%d" % db.opinion.count())


# 用户评论入库
db.ugc.remove()
data = csv.reader(file('static/data/raw/ugc.csv', 'rb'))
for line in data:
    if data.line_num == 1:
            continue
    item = dict()
    item['_id'] = line[0].decode('utf-8')
    item['item_type'] = line[1].decode('utf-8')
    item['source'] = line[2].decode('utf-8')
    item['url'] = line[3].decode('utf-8')
    item['author'] = line[4].decode('utf-8')
    item['title'] = line[5].decode('utf-8')
    item['content'] = line[6].decode('utf-8')
    item['item_pub_time'] = line[7].decode('utf-8')
    item['tags'] = line[8].decode('utf-8')
    item['cmt_cnt'] = line[9].decode('utf-8')
    item['fav_cnt'] = line[10].decode('utf-8')
    item['gmt_create'] = line[11].decode('utf-8')
    item['exinfo1'] = line[12].decode('utf-8')
    item['exinfo2'] = line[13].decode('utf-8')
    db.ugc.insert(item)
print("now the number of ugc is:%d" % db.ugc.count())

# 初始用户
db.user.remove();
db.user.insert({'username': 'mdw', 'password': '123','platform_names': [u'拍拍贷']})
print("now the number of user is:%d" % db.user.count())
