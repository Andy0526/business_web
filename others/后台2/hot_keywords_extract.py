#encoding=utf8
'''
    __author__ = 'Administrator'
    2016.3.13 16:30 first version
    分词、提取关键字、提取每天热门关键字
'''

import csv
import json
import time
import re
from string import punctuation,digits,letters,whitespace
import sys
import datetime
from helper import myio
import jieba
import jieba.analyse
import math
import pandas as pd
from gensim import corpora,models
from helper.textprocessing import handleContent
from pymongo import MongoClient
client=MongoClient()
reload(sys)
sys.setdefaultencoding('utf-8')





print "before load date", datetime.datetime.now()
news_dataset = pd.read_pickle("./data/news_dataset.pkl")
print "end load date", datetime.datetime.now()


text_tags = []
lda_train_set = []

## 8000 articles 5mins
print "before cut segments", datetime.datetime.now()


'''
    pd_docs pandas.Dataframe
    time_begin str
    time_end str
    return list of pairs of key words and weights
'''
def getKeyword_times(pd_docs, time_begin, time_end):
    time_begin = datetime.datetime.strftime(time_begin, '%Y-%m-%d')
    time_end = datetime.datetime.strftime(time_end, '%Y-%m-%d')
    docs = pd_docs[pd_docs.item_pub_time >= time_begin]
    docs = docs[docs.item_pub_time <= time_end]
    keyword_dict = {}
    for i in xrange(0, len(docs)):
        title = docs.iloc[i]["title"]
        title = handleContent(title)
        title_keyword =  list(jieba.cut(title, cut_all=False))
        content = docs.iloc[i]["content"]
        content = handleContent(content)
        cont_keyword = jieba.analyse.extract_tags(content, topK = 100)
        for kw in title_keyword:
            if  kw.isdigit() == True or len(kw) <= 1:
                continue
            keyword_dict[kw] = keyword_dict.setdefault(kw, 0) + 2
        for kw in cont_keyword:
            if  kw.isdigit() == True or len(kw) <= 1:
                continue
            keyword_dict[kw] = keyword_dict.setdefault(kw, 0) + 1
    return sorted(keyword_dict.items(), lambda a,b:-cmp(a[1], b[1]))


def getKeyword_time(pd_docs, dt = None):
    kw_data = {}
    dt_str = datetime.datetime.strftime(dt, "%Y-%m-%d")
    kw_data.setdefault("dt", dt_str)
    d_end = dt + datetime.timedelta(days=1)
    keyword_list = getKeyword_times(pd_docs, dt, d_end)[:100]
    if len(keyword_list) <= 1:
        print "day of " + dt_str + " had no news"
        return
    day_keywords = ""
    for pp in keyword_list:
        day_keywords += str(pp[0]) + ":" + str(pp[1]) + ";"
    kw_data.setdefault("day_keywords", day_keywords[:-1])

    db = client.holmesdb
    t_sh_industry_keywords = db.t_sh_industry_keywords
    if t_sh_industry_keywords.find_one(kw_data) == None:
        id = t_sh_industry_keywords.insert_one(kw_data).inserted_id
    #print t_sh_industry_keywords.find_one({"dt": dt_str})

    #day_keyword_list
    return keyword_list


def sigmoid(x):
    return 1.0 / (1 + math.exp(-x))

def extract_hot_keywords(cur_d, date_begin, keyword_rev_dict, delta):
    pre_d = cur_d - datetime.timedelta(days=delta)
    keyword_list = getKeyword_times(news_dataset, pre_d, cur_d)
    new_keyword_list = []
    ## time delta转int
    if pre_d <= date_begin:
        all_date = 1
    else:
        all_date = int(str(pre_d - date_begin).split(' ')[0])
    #print cur_d, date_begin, all_date
    for (word, weight) in keyword_list:
        prev_cnt = 0
        if word in keyword_rev_dict:
            for (d, w) in keyword_rev_dict[word]:
                if d < cur_d:
                    prev_cnt += 1
                else:
                    break
        weight = weight * 1.0 / all_date * math.log(all_date * 1.0 / (1 + prev_cnt))
        new_keyword_list.append((word, weight))
    new_keyword_list =  sorted(new_keyword_list, lambda a,b: -cmp(a[1], b[1]))[:100]
    return new_keyword_list



date_begin =  datetime.date(2014, 12, 1)
date_end   =  datetime.date(2016, 03, 01)
#每次重新建立每天关键字库，并建立词的倒排表
# client.holmesdb.t_sh_industry_keywords.remove()

all_keyword_list = []
keyword_rev_dict = {}
keyword_rev_str_dict = {}
##提取每日关键字
for i in range(3650):
    d = date_begin + datetime.timedelta(days=i)
    if d > date_end: break
    keyword_list = getKeyword_time(news_dataset, d)
    if keyword_list == None:
        continue
    all_keyword_list.append(keyword_list)
    for (word, weight) in keyword_list:
        keyword_rev_dict.setdefault(word, [])
        keyword_rev_str_dict.setdefault(word, [])
        keyword_rev_dict[word].append((d, weight))
        d_str = datetime.datetime.strftime(d, '%Y-%m-%d')
        keyword_rev_str_dict[word].append((d_str, weight))
myio.writeJsonDict(keyword_rev_str_dict, open("./data/keyword_revise_dict.json", "w"))

##提取每日热门关键字和近期热门关键字
for i in range(3650):
    cur_d = date_begin + datetime.timedelta(days=i)
    if cur_d > date_end:
        break

    ## 提取每天关键字
    new_keyword_list = extract_hot_keywords(cur_d, date_begin, keyword_rev_dict, 1)
    kw_data = {}
    kw_data.setdefault("dt", datetime.datetime.strftime(cur_d, "%Y-%m-%d"))
    day_keywords = ""
    for pp in new_keyword_list:
        day_keywords += str(pp[0]) + ":" + str(pp[1]) + ";"
    kw_data.setdefault("day_hot_keywords", day_keywords[:-1])
    db = client.holmesdb
    t_sh_industry_keywords = db.t_sh_industry_keywords
    if t_sh_industry_keywords.find_one(kw_data) == None:
        #print kw_data
        id = t_sh_industry_keywords.insert_one(kw_data).inserted_id

    ## 提取每周关键字
    new_keyword_list = extract_hot_keywords(cur_d, date_begin, keyword_rev_dict, 7)
    kw_data = {}
    kw_data.setdefault("dt", datetime.datetime.strftime(cur_d, "%Y-%m-%d"))
    week_keywords = ""
    for pp in new_keyword_list:
        week_keywords += str(pp[0]) + ":" + str(pp[1]) + ";"
    kw_data.setdefault("week_hot_keywords", week_keywords[:-1])
    db = client.holmesdb
    t_sh_industry_keywords = db.t_sh_industry_keywords
    if t_sh_industry_keywords.find_one(kw_data) == None:
        #print kw_data
        id = t_sh_industry_keywords.insert_one(kw_data).inserted_id

    ## 提取每周关键字
    new_keyword_list = extract_hot_keywords(cur_d, date_begin, keyword_rev_dict, 30)
    kw_data = {}
    kw_data.setdefault("dt", datetime.datetime.strftime(cur_d, "%Y-%m-%d"))
    week_keywords = ""
    for pp in new_keyword_list:
        week_keywords += str(pp[0]) + ":" + str(pp[1]) + ";"
    kw_data.setdefault("month_hot_keywords", week_keywords[:-1])
    db = client.holmesdb
    t_sh_industry_keywords = db.t_sh_industry_keywords
    if t_sh_industry_keywords.find_one(kw_data) == None:
        #print kw_data
        id = t_sh_industry_keywords.insert_one(kw_data).inserted_id

#查看每天、每周的热点词
test_date = datetime.date(2015, 12, 18)
test_date_end = test_date + datetime.timedelta(days=7)
keyword_list = getKeyword_times(news_dataset, test_date, test_date_end)
new_keyword_list = []
all_date = int(str(test_date - date_begin).split(' ')[0])
for (word, weight) in keyword_list:
    prev_cnt = 0
    if word in keyword_rev_dict:
        for (d, w) in keyword_rev_dict[word]:
            if d < test_date:
                prev_cnt += 1
            else:
                break
    # print word, weight, prev_cnt,
    weight = weight * 1.0 / all_date * math.log(all_date * 1.0 / (1 + prev_cnt))
    # print weight
    new_keyword_list.append((word, weight))
new_keyword_list =  sorted(new_keyword_list, lambda a,b: -cmp(a[1], b[1]))
for pp in new_keyword_list:
    print pp[0],pp[1]
# 分词，关键字提取
keyword_dict = {}
day_cnt = {}
