#encoding=utf8
'''
    __author__ = 'Administrator'
    2016.4.10 20:30 first version
    提取三大门户新闻网+财新网中的P2P资讯
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


p2p_key_list = [line.strip() for line in open("../data/key_list_hot.txt")]

columns = "item_id,item_type,source,url,author,title,content,item_pub_time,tags,cmt_cnt,fav_cnt,gmt_create,exinfo1,exinfo2".split(',')
item_id_dict = {}
writer = csv.writer(file("../data/news/news_other.csv", 'wb'))
writer.writerow(columns)

news_cnt = 0
news_other_dir = "../data/news/news_other"
date_dict = {}
month_dict = {}
for cur,dirnames,filenames in os.walk(news_other_dir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for f in os.listdir(cur):
        print f
        # if f.find("weixin") == -1:
        #     continue
        news_cnt = 0
        f_in = csv.reader(file(news_other_dir + r"/" + f, "r"))
        lines = [line for line in f_in]
        print len(lines)
        for line in lines[1:]:
            if len(line) < 14:
                continue
            if len(line) > 14:
                line = line[:14]
            #content = line[6].replace("###r###", "\r").replace("###n###", "\n").replace("###t###", "\t")
            content = line[6]
            title = line[5]

            for key in p2p_key_list:
                if title.find(key) != -1 or content.find(key) != -1:
                    #print title
                    #print content
                    writer.writerow(line)
                    #if f == 'caixin.csv':
                        #print key
                        #print title, content
                    news_cnt += 1
                    dt = line[7]
                    m = dt[:8]
                    date_dict[dt] = date_dict.setdefault(dt, 0) + 1
                    month_dict[m] = month_dict.setdefault(m, 0) + 1
                    break
        print news_cnt
print date_dict
print month_dict