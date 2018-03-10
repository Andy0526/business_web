#encoding=utf8
'''
    __author__ = 'Administrator'
    2016.3.6 18:26 first version
    舆情大盘数据汇总，并存入数据库holmesdb
'''

import csv
import json
import time
import re
from string import punctuation,digits,letters,whitespace
import sys
import datetime

import jieba
import jieba.analyse
import pandas as pd
from gensim import corpora,models
from helper.textprocessing import handleContent
from pymongo import MongoClient
client=MongoClient()
reload(sys)
sys.setdefaultencoding('utf-8')
jieba.load_userdict("C:/Python27/Lib/site-packages/jieba-0.37-py2.7.egg/jieba/financedict.txt")



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
article_res = [news_res, policy_res, ugc_res, expert_res]
key = ["news", "policy", "ugc", "expert"]
month_summary = {}
month12_day_summary = {}
source_summary = {}
for i in xrange(4):
    for res in article_res[i]:
        if res['item_pub_time'] >= '2015-01-01' and res['item_pub_time'] <= '2015-12-31':
            title = res['title']
            content = res['content']
            t = res['item_pub_time']
            m = t[5:7]
            date = t[5:].replace("-", ".").split(" ")[0]
            #print m, date
            month_summary[m][key[i]] = month_summary.setdefault(m , {}).setdefault(key[i], 0) + 1
            if date >= '12.01' and date <= '12.31':
                month12_day_summary[date][key[i]] = month12_day_summary.setdefault(date , {}).setdefault(key[i], 0) + 1
                source = res['source']
                if source == "和讯P2P政策":
                    source = "和讯P2P"
                if source == 'zhongshen':
                    source = '中申网'
                source_summary[source] = source_summary.setdefault(source, 0) + 1

print month_summary
print month12_day_summary
for source in source_summary:
    print source, source_summary[source]

def writeJsonDict(person, f_out):
    outStr = json.dumps(person, ensure_ascii = False)        		#处理完之后重新转为Json格式
    f_out.write(outStr.encode('utf-8') + '\n')          			#写回到一个新的Json文件中去

print "begin save datas", datetime.datetime.now()
writeJsonDict(month_summary, open("./data/summary/month_summary.json", "w"))
writeJsonDict(month12_day_summary, open("./data/summary/month12_day_summary.json", "w"))
writeJsonDict(source_summary, open("./data/summary/source_summary.json", "w"))

pos_weight = [0.37, 0.43, 0.42, 0.45, 0.43, 0.44, 0.42, 0.4, 0.39, 0.387,\
    0.38, 0.378, 0.376, 0.365, 0.33, 0.274, 0.25, 0.26, 0.35, 0.42,\
    0.41, 0.47, 0.43, 0.46, 0.47, 0.43, 0.44, 0.45, 0.463, 0.456, \
    0.465
    ]
sa_month12_day_summary = {}
for dt in month12_day_summary:
    cnt = month12_day_summary[dt]["ugc"]
    cnt_pos = int(cnt * pos_weight[int(dt[3:])-1])
    cnt_nag = int(cnt - cnt_pos)
    sa_month12_day_summary.setdefault(dt, {"pos":cnt_pos, "nag":cnt_nag})
writeJsonDict(sa_month12_day_summary, open("./data/summary/sa_month12_day_summary.json", "w"))

print "end save datas", datetime.datetime.now()