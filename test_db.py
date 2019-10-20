# -*- coding: utf-8 -*-

from pymongo import MongoClient

# 连接
conn = MongoClient('localhost', 27017)
db = conn.p2p


def sign_in_valid(userName, password):
    result = db.user.find_one({'username': userName, 'password': password})
    print(result['platform_name'])


result = db.user.find()
for r in result:
    print(r)
sign_in_valid('mdw', '123')

ls = []
ls.append("mi")
print(ls)
ls.remove("mi")
print(ls)
