#encoding=utf8
'''
    __author__ = 'Administrator'
    2016.3.3 20:30 first version
    加载文件
'''

import csv
import json
import time
import re
from string import punctuation,digits,letters,whitespace
import sys
import os
import datetime
from bson import ObjectId
import jieba
import jieba.analyse
import pandas as pd
import pymongo
from pymongo import MongoClient
client=MongoClient()
reload(sys)
sys.setdefaultencoding('utf-8')
csv.field_size_limit(sys.maxint)



def handleContent(string):
    """字符串处理，去标点符号，中文分词，return:unicode"""
    string = string.decode('utf-8')
    #针对自己的文本数据定制化修改
    string = string.replace("<p>", "").replace("</p>", "").replace("<strong>", "").replace("</strong>", "")
    string = string.replace("#r#", "\n").replace("#n#", "\n").replace("", "")
    string = string.replace(" ", "").replace("\n", "").replace("\t", " ")

    string = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！：》，《”。“？、~@#￥%……&*（）]+".decode("utf-8"), "".decode("utf-8"),string)
    string = string.encode('utf-8')
    string = string.translate(None,punctuation+digits+letters+whitespace)
    return string

def getJsonFile(json_fname):
    json_file = file(json_fname, "r")
    json_vector = []
    for line in json_file:
         person_info = json.loads(line)
         json_vector.append(person_info)
    return json_vector

def getTable_maxID(mongodb_table, field):
    try:
        res = mongodb_table.find().sort(field, pymongo.DESCENDING)[0]
        if res == None:
            return 0
        return int(res[field])
    except:
        return 0

def insertDB(mongodb_table, line, cols):
    try:
        ori = cols[0]
        cols[0] = "_id"
        data = {}
        for i in xrange(0, len(cols)):
            data.setdefault(cols[i], line[i])
        mongodb_table.insert(data)
        cols[0] = ori
    except Exception :
         cols[0] = ori
         print Exception
         return

print "before load data", datetime.datetime.now()
# 数据加载
news_title_dict = {}
texts_news = []
texts_news_other = []
texts_ugc = []
texts_experts = []
texts_policy = []
texts_nlp_train = []

db = client.holmesdb
t_news = db.t_news_di
t_news.remove()
t_news_id = getTable_maxID(t_news, "_id")
#news & policy
columns = []
dir_list = ["./data/news"]
for dir in dir_list:
    print dir
    for fname in os.listdir(dir):
        if fname.find(".csv") != -1:
            fname = fname.decode("gbk")
            f_in = csv.reader(file(dir + r"/" + fname, "r"))
            lines = [line for line in f_in]
            if len(columns) == 0:
                columns = lines[0]
            for line in lines[1:]:
                if len(line) < 14:
                    continue
                if len(line) > 14:
                    line = line[:14]
                texts_news.append(line)
                line[6] = line[6].replace("###r###", "\r").replace("###n###", "\n").replace("###t###", "\t")
                title = line[5]
                if title not in news_title_dict:
                    news_title_dict.setdefault(title, 0)
                    line[0] = str(t_news_id )
                    t_news_id  += 1
                    insertDB(t_news, line, columns)
print len(news_title_dict)
print columns
data = pd.DataFrame(texts_news)
data.columns = columns
pd.to_pickle(data,  'data/news_dataset.pkl')

