#encoding=utf8
'''
    __author__ = 'Administrator'
    2016.4.2 14:11 first version
    问题平台分析
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
from helper import myio

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
def getJsonFile_line(json_fname):
    json_file = file(json_fname, "r")
    json_vector = []
    for line in json_file:
         person_info = json.loads(line)
         json_vector.append(person_info)
    return json_vector
def getJsonFile_all(json_fname):
    json_file = open(json_fname, "r")
    dict = json.load(json_file)
    json_file.close()
    return dict

print "before load bad company datas", datetime.datetime.now()
db = client.holmesdb
t_news = db.t_news_di
t_policy = db.t_policy_di
t_ugc = db.t_ugc_di
t_expert = db.t_expert_opinion_di
t_news_caixin = db.t_news_caixin_di
news_res = t_news.find()
policy_res = t_policy.find()
ugc_res = t_ugc.find()
expert_res = t_expert.find()

bad_company_2015 = getJsonFile_all("./data/bad_platform/bad_platform_2015.json")
print "end load bad company datas", datetime.datetime.now()


article_res = [news_res, policy_res, expert_res, ugc_res]
for data_set in article_res:
    print data_set.count(),
print ""
key = ["news", "policy", "expert", "ugc"]
month_summary = {}
for i in xrange(len(article_res)):
    for res in article_res[i]:
        if res['item_pub_time'] >= '2014-01-01' and res['item_pub_time'] <= '2015-12-31':
            title = res['title']
            content = res['content']
            t = res['item_pub_time']
            m = t[0:7].replace("-", ".")
            date = t[5:].replace("-", ".").split(" ")[0]
            for pjson in bad_company_2015:
                pname = pjson['platform_name']
                if content.find(pname) != -1 or content.find(pname) != -1:
                    month_summary[pname][m] = month_summary.setdefault(pname, {}).setdefault(m, 0) + 1
                    #print pname, m, month_summary[pname][m]
bad_platform_trend = {}
for pjson in bad_company_2015:
    pname = pjson['platform_name']
    pro_date = pjson['problem_time']
    last_year_date = "2014." + pro_date[5:7]
    sum_cnt = 0
    p_trend = []
    if pname in month_summary:
        month_data = sorted(month_summary[pname].items(), lambda a, b: cmp(a[0], b[0]))
        for (m, cnt) in month_data:
            print pname, m, pro_date, last_year_date
            if m >= last_year_date and m < pro_date:
                try:
                    y1, m1 = int(m[:4]), int(m[5:])
                    y2, m2 = int(pro_date[:4]), int(pro_date[5:])
                    delta = (y2 - y1) * 12 + m2  - m1
                    sum_cnt += cnt
                    p_trend.append((delta, cnt))
                except Exception:
                    print Exception
                    continue
        if sum_cnt >= 20:
            print pname, pro_date, p_trend
            bad_platform_trend.setdefault(pname, [pro_date, p_trend])
myio.writeJsonDict(bad_platform_trend, open("./data/bad_platform/bad_platform_trend.json", "w"), "rows")
print "end analyze bad company datas", datetime.datetime.now()


