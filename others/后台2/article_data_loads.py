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
import article_classify
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
         print line
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
t_policy = db.t_policy_di
t_ugc = db.t_ugc_di
t_expert = db.t_expert_opinion_di
t_news_caixin = db.t_news_caixin_di
# t_news.remove()
# t_policy.remove()
# t_expert.remove()
# t_ugc.remove()
t_news_id = getTable_maxID(t_news, "_id")
t_policy_id = getTable_maxID(t_policy, "_id")
t_expert_id = getTable_maxID(t_expert, "_id")
t_ugc_id = getTable_maxID(t_ugc, "_id")
t_news_caixin_id = getTable_maxID(t_news_caixin, "_id")
print "max_id:", t_news_id, t_policy_id, t_expert_id,t_ugc_id
#news & policy
columns = []
dir_list = ["./data/news", "./data/policy"]
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
                line[6] = line[6].replace("###r###", "\r").replace("###n###", "\n").replace("###t###", "\t")
                line[6] = line[6].replace("#r#", "\r").replace("#n#", "\n").replace("#t#", "\t")
                title = line[5]
                item_pub_time = line[7]
                if item_pub_time.find(" ") != -1:
                    line[7] = item_pub_time[:item_pub_time.find(" ")]
                content = line[6]
                line[8] = article_classify.getArticleTag(title, content)
                # print title
                texts_news.append(line)
                if dir == dir_list[1]:          ##policy
                    texts_policy.append(line)
                    if title not in news_title_dict:
                        news_title_dict.setdefault(title, 0)
                        line[0] = str(t_policy_id )
                        t_policy_id += 1
                        #insertDB(t_policy, line, columns)

                else:                       ##news
                    if title not in news_title_dict:
                        news_title_dict.setdefault(title, 0)
                        line[0] = str(t_news_id )
                        t_news_id  += 1
                        #insertDB(t_news, line, columns)
            texts_nlp_train.append(line)
#ugc & experts
dir_list = ["./data/ugc_opinion_comment", "./data/expert_opinions"]
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
                line[6] = line[6].replace("###r###", "\r").replace("###n###", "\n").replace("###t###", "\t")
                line[6] = line[6].replace("#r#", "\r").replace("#n#", "\n").replace("#t#", "\t")
                title = line[6]
                item_pub_time = line[7]
                if item_pub_time.find(" ") != -1:
                    line[7] = item_pub_time[:item_pub_time.find(" ")]
                content = line[6]
                line[8] = article_classify.getArticleTag(title, content)
                if dir == dir_list[0]:
                    texts_ugc.append(line)
                    line[0] = str(t_ugc_id)
                    t_ugc_id += 1
                    #insertDB(t_ugc, line, columns)
                if dir == dir_list[1]:
                    texts_experts.append(line)
                    line[0] = str(t_expert_id )
                    t_expert_id += 1
                    #insertDB(t_expert, line, columns)
                texts_nlp_train.append(line)

print len(texts_news), len(texts_policy), len(texts_ugc), len(texts_experts), len(texts_nlp_train)
print len(columns)
data_list = [texts_news, texts_policy, texts_ugc, texts_experts, texts_nlp_train]
fname_list = ["data/news_dataset.pkl", "data/policy_dataset.pkl", "data/ugc_dataset.pkl", "data/experts_dataset.pkl", "data/nlp_train_dataset.pkl"  ]
assert len(data_list) == len(fname_list)
for i in xrange(len(data_list)):
    try:
        data = pd.DataFrame(data_list[i])
        data.columns = columns
        pd.to_pickle(data,  fname_list[i])
    except Exception:
        print i, fname_list[i], Exception
        continue
print "before load data", datetime.datetime.now()