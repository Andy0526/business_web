#encoding=utf8
'''
    __author__ = 'Administrator'
    2016.3.3 20:30 first version
    加载文件
'''
import csv
import json
import os
import time
import re
from string import punctuation,digits,letters,whitespace
import sys
import datetime
from helper import myio
import jieba
import jieba.analyse
import math
from helper import myio
import pandas as pd
from gensim import corpora,models
from helper.textprocessing import handleContent
from pymongo import MongoClient
client=MongoClient()
db = client.holmesdb
reload(sys)
sys.setdefaultencoding('utf-8')
stop_dict = {}
for line in open("C:\Python27\Lib\site-packages\jieba-0.37-py2.7.egg\jieba\stop_chinese.txt"):
    stop_dict.setdefault(line.strip(), 0)


platform_json = myio.getJsonFile_all('./data/platform_company/display_platform.json')
platform_name_list = platform_json.keys()


print "before load date", datetime.datetime.now()
news_dataset = pd.read_pickle("./data/news_dataset.pkl")
all_dataset = news_dataset
all_doc_cnt = len(news_dataset)
print "end load date", datetime.datetime.now()


print "before cut segments", datetime.datetime.now()
# 分词，关键字提取
df_dict = {}
for i in xrange(0, all_doc_cnt):#len(all_dataset)):
    title = all_dataset.iloc[i]['title']
    content = all_dataset.iloc[i]['content']
    item_pub_time = all_dataset.iloc[i]['item_pub_time']
    doc =  handleContent(title) + " " + handleContent(content)
    tokens = list(jieba.cut(doc))
    new_tokens = []

    token_dict_delta = {}
    for i in xrange( len(tokens) ):
        if tokens[i].isdigit() == True or len(tokens[i]) <= 1\
            or (tokens[i].isalnum() == True and len(tokens[i]) > 20):
             #print tokens[i],
             continue
        if tokens[i] in stop_dict:#去停用词
            continue
        new_tokens.append(tokens[i])
        token_dict_delta.setdefault(tokens[i], 0)
    for token in token_dict_delta:
        df_dict[token] = df_dict.setdefault(token, 0) + 1
print "all word cnt:" , len(df_dict)
t_word_df_dd = db.t_word_df_dd
t_word_df_dd.remove()
for token in df_dict:
    t_word_df_dd.insert({"word":token, "df":df_dict[token]})

t_word_df_dd = db.t_word_df_dd
t_news = db.t_news_di
news_res = t_news.find({"item_pub_time": {"$lt": '2016-01-05', "$gt": '2015-11-25'}})
print "month news cnt:", news_res.count()
platform_key_dict = {}
for news in news_res:
    title = news['title']
    content = news['content']
    doc =  handleContent(title) + " " + handleContent(content)
    tokens = list(jieba.cut(doc))
    token_dict = {}
    for i in xrange( len(tokens) ):
        if tokens[i].isdigit() == True or len(tokens[i]) <= 1\
                or (tokens[i].isalnum() == True and len(tokens[i]) > 20):
             #print tokens[i],
             continue
        if tokens[i] in stop_dict:#去停用词
            continue
        token_dict[tokens[i]] = token_dict.setdefault(tokens[i], 0) + 1
    token_w_list = []
    for token in token_dict:
        tf = token_dict[token]
        # df = t_word_df_dd.find_one({"word":token})
        # df = df["df"] if df != None else 0
        df = df_dict[token] if token in df_dict else 0
        tfidf = math.log(1+tf) * math.log((1+all_doc_cnt) * 1.0 / (1+df))
        token_w_list.append((token, tfidf))
    news_key_list = sorted(token_w_list, lambda a,b: -cmp(a[1], b[1]))[:20]
    p_cnt = 0
    for pname in platform_name_list:
        if doc.find(pname) != -1:
            p_cnt += 1
    for pname in platform_name_list:
        if title.find(pname) != -1:
            for (key, w) in news_key_list:
                if key != pname:
                    #print pname, key, w
                    platform_key_dict[pname][key] = platform_key_dict.setdefault(pname, {}).setdefault(key, 0) + w * 1.0 / p_cnt

platform_key_month12 = {}
f_path = "./data/platform_company/platform_news_keywords"
for pname in platform_name_list:
    if pname in platform_key_dict:
        hot_key_list = sorted(platform_key_dict[pname].items(), lambda a,b: -cmp(a[1], b[1]))[:50]
        print pname
        for (hot_key, w) in hot_key_list:
            print hot_key,
        print ""
        platform_key_month12.setdefault(pname, hot_key_list)
myio.writeJsonDict(platform_key_month12, open(f_path, "w"), "rows")

