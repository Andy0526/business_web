#encoding=utf8
'''
    __author__ = 'Administrator'
    2016.4.14 01:05 first version
    资讯分类，类别包括：
        高层变动、新产品、平台跑路、提现困难、相关指标、
'''

import csv
import json
import time
import re
from string import punctuation,digits,letters,whitespace
import sys
import os
import datetime
import jieba
import jieba.analyse
import pandas as pd
import types
from pymongo import MongoClient
client=MongoClient()
reload(sys)
sys.setdefaultencoding('utf-8')
csv.field_size_limit(sys.maxint)



#tag 高层变动
def getArticleTag(title, content):
    recall_key_list = {
        '高层变动':{'高层变动', '高管变动', '换人', '离职'},\
        '新产品':{'新产品', '产品上市'},\
        '平台跑路':{'平台跑路', '跑路'},\
        '提现困难':{'提现困难', '无法兑付'},\
        '平台融资':{'A轮融资', 'B轮融资',  'C轮融资',  'D轮融资',  'E轮融资', '估值', 'IPO', '上市'}\
    }
    tag_list = ''
    for tag in recall_key_list:
        for key in recall_key_list[tag]:
            if title.find(key) != -1 or content.find(key) != -1:
                tag_list += tag + ','
                break
    if tag_list != '':
        tag_list = tag_list[:-1]
        # print title, tag_list
    return tag_list


if __name__ == "__main__":
    db = client.holmesdb
    t_news = db.t_news_di
    t_news_res = t_news.find()
    for news in t_news_res:
        title = news['title']
        content = news['content']
        flag = getArticleTag(title, content)

