#encoding=utf8
'''
    __author__ = 'Administrator'
    2016.2.27 20:30 first version
    分词、提取关键字、提取文章主题
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
news_dataset_other = pd.read_pickle("./data/news_dataset_other.pkl")
all_dataset = pd.concat([news_dataset, news_dataset_other])
print "end load date", datetime.datetime.now()


# 分词，关键字提取
text_tags = []
lda_train_set = []
keyword_dict = {}
day_cnt = {}


for item_pub_time in all_dataset['item_pub_time']:
    day_cnt[item_pub_time[:10]] = day_cnt.setdefault(item_pub_time[:10], 0) + 1
day_cnt =  sorted(day_cnt.items(), lambda a, b: -cmp(a[0], b[0]))
f_out = open("data/everyday_newscnt.txt", "w")
for pp in day_cnt:
    if len(pp[0]) >= 1 and str(pp[0][0]).isdigit() == True:
        f_out.write("%s %s\n"%(pp[0], pp[1]))

print "before cut segments", time.localtime()
for row_id, news in all_dataset.iterrows():
    if row_id % 1000 == 999:
        print row_id
    content = news['content']
    content = handleContent(content)
    pub_time = news['item_pub_time']
    content = content.replace(" ", "").replace("\n", "").replace("　", "")
    seg = list(jieba.cut(content))

    lda_train_set.append(seg)
    key_words = jieba.analyse.extract_tags(content, topK = 20)
    for token in key_words:
        keyword_dict[token] = keyword_dict.setdefault(token, 0) + 1
    text_tags.append(key_words)



print "end cut segments", time.localtime()


for keyword in key_words:
    print keyword

