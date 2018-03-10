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

import jieba
import jieba.analyse
import math
import pandas as pd
from gensim import corpora,models
from helper.textprocessing import handleContent
from pymongo import MongoClient
reload(sys)
sys.setdefaultencoding('utf-8')



def handleContent(string):
    """字符串处理，去标点符号，中文分词，return:unicode"""
    string = string.decode('utf-8')
    #针对自己的文本数据定制化修改
    string = string.replace("<p>", "").replace("</p>", "").replace("<strong>", "").replace("</strong>", "")
    string = string.replace("#r#", "\r").replace("#n#", "\n").replace("#t#", "\t")
    string = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！：》，《”。“？、~@#￥%……&*（）]+".decode("utf-8"), "".decode("utf-8"),string)
    string = string.encode('utf-8')
    string = string.translate(None,punctuation+whitespace)
    return string

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