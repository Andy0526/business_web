#encoding=utf8
'''
    __author__ = 'Administrator'
    2016.3.13 18:23 first version
    1、为每个ugc计算质量分
        质量分: 考虑因素 1、整体长度 2、每个语句的长度是否相近 3、由新闻生成过来的概率
        概率分有做归一化
    2、高质量的ugc转为news
'''
import csv
import json
import os
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

stop_dict = {}
for line in open("C:\Python27\Lib\site-packages\jieba-0.37-py2.7.egg\jieba\stop_chinese.txt"):
    stop_dict.setdefault(line.strip(), 0)

print "before load date", datetime.datetime.now()
#train data
news_dataset = pd.read_pickle("./data/news_dataset.pkl")
experts_dataset = pd.read_pickle("./data/experts_dataset.pkl")
train_dataset = pd.concat([news_dataset, experts_dataset])
# news_dataset = pd.read_pickle("./data/news_dataset.pkl")
# news_dataset_other = pd.read_pickle("./data/news_dataset_other.pkl")
# experts_dataset = pd.read_pickle("./data/experts_dataset.pkl")
# train_dataset = pd.concat([news_dataset, news_dataset_other])
# train_dataset = pd.concat([train_dataset, experts_dataset])
#ugc
ugc_dataset = pd.read_pickle("./data/ugc_dataset.pkl")
print "end load date", datetime.datetime.now()

# 以字典方式读取文件
def read_dict(file_path):
    try:
        file_r = open(file_path, 'r')
        import pickle

        dic_t = dict(pickle.load(file_r))
        file_r.close()
        return dic_t
    except Exception, e:
        print e.message
        return {}
# 文件写出，主要是字典文件
def write_dic(obj, file_path):
    try:
        file_w = open(file_path, 'w')
        import pickle

        pickle.dump(obj, file_w)
        file_w.close()
    except Exception, e:
        print e.message



min_len = 999999999999
max_len = 0
term_frequcy_path = 'data/term_frequecy.pkl'
bigram_frequecy_path = 'data/bigram_frequecy.pkl'
print "begin build bigram dict date", datetime.datetime.now()
if os.path.exists(bigram_frequecy_path) == True and os.path.exists(term_frequcy_path):
    term_frequcy = read_dict(term_frequcy_path)
    bigram_frequecy = read_dict(bigram_frequecy_path)
else:
    ugc_quality_train = []
    term_frequcy = {}
    bigram_frequecy = {}
    line_cnt = 0
    for content in train_dataset['content']:
        line_cnt += 1
        if line_cnt >= 10000:
            break
        content = handleContent(content)
        tokens = list(jieba.cut(content))
        if len(tokens) < min_len:
            min_len = len(tokens)
        if len(tokens) > max_len:
            max_len = len(tokens)
        for term in tokens:
            term_frequcy[term] = term_frequcy.setdefault(term, 0) + 1
        for i in xrange(0, len(tokens)-1):
            bigram_frequecy[tokens[i]][tokens[i+1]] = bigram_frequecy.setdefault(tokens[i], {}).setdefault(tokens[i+1], 0) + 1
        ugc_quality_train.append(tokens)

    write_dic(term_frequcy,  'data/term_frequcy.pkl')
    write_dic(bigram_frequecy,  'data/bigram_frequecy.pkl')
# 80281 80131
print len(term_frequcy), len(bigram_frequecy)
total_count = 0
for term in term_frequcy:
    total_count += term_frequcy[term]
bigram_count = 0
for term in bigram_frequecy:
    bigram_count += len(bigram_frequecy[term])
print total_count, bigram_count

print "end build bigram dict date", datetime.datetime.now()


print "begin get ugc quality date", datetime.datetime.now()
test_list = []
min_quality = 1
max_quality = 0
min_sen_cnt = 9999999
max_sen_cnt = 0
for i in xrange(0, 10000):#len(ugc_dataset)):
    quality = 0.0
    title = ugc_dataset.iloc[i]['title']
    content = ugc_dataset.iloc[i]['content']
    content = content.replace("#n#", "。")
    sentences = content.split("。")
    sen_cnt = len(content.split("。"))
    if sen_cnt < min_sen_cnt:
        min_sen_cnt = sen_cnt
    if sen_cnt > max_sen_cnt:
        max_sen_cnt = sen_cnt
    # doc =  handleContent(title) + " " + handleContent(content)
    content = handleContent(content)
    tokens = list(jieba.cut(content))
    if len(tokens) == 0:
        continue
    if tokens[0] in term_frequcy:
        base = (term_frequcy[tokens[0]] + 1) * 1.0 / (1 + total_count)
    else:
        base = 1.0 / (1 + total_count)
    for i in xrange(1, len(tokens)-1):
        t1 = tokens[i-1]
        t2 = tokens[i]
        if t1 in bigram_frequecy and t2 in bigram_frequecy[t1]:
            base *= (1 + bigram_frequecy[t1][t2]) * 1.0 / (1 + term_frequcy[t1])
        elif t1 in term_frequcy:
            base *= 1.0 / (1 + term_frequcy[t1])
        else:
            base *= 1.0 / bigram_count
    base *= len(tokens)
    if base < min_quality:
        min_quality = base
    if base > max_quality:
        max_quality = base
    test_list.append((title, content, base, len(tokens), sen_cnt ))


if max_len > 5000: max_len = 5000
if max_sen_cnt > 500: max_sen_cnt = 500
print min_len, max_len, min_sen_cnt, max_sen_cnt, min_quality, max_quality
count_list = [0] * 200
for (title, content, gram_w, length, sen_cnt) in test_list :
    if length < 1:
        quality = 0.0001
    else:
        len_weight = (length - min_len + 0.001) * 1.0 / max_len
        if len_weight > 1.0: len_weight = 1
        gram_weight = (gram_w - min_quality) / max_quality
        sen_weight = (sen_cnt - min_sen_cnt) / max_sen_cnt
        quality = gram_weight * 0.8 + len_weight * 0.1  + sen_weight * 0.1
    if quality > 0.0:
        print title, content, gram_w, length, sen_cnt, gram_weight, len_weight, sen_weight, quality
        print ""
    for i in xrange(1, 101):
        if quality >= 0.0001 * i:
            count_list[i] += 1
for i in xrange(0, 101):
    if count_list[i] > 0:
        print i * 0.001, count_list[i]
print "end get ugc quality date", datetime.datetime.now()

