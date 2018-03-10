#encoding=utf8
'''
    __author__ = 'Administrator'
    2016.3.6 18:26 first version
    行业的所有数据汇总，并存入数据库holmesdb
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



area_data = pd.read_csv("./data/platform_company/industry_areas.csv")
db = client.holmesdb
t_sh_industry_areas = db.t_sh_industry_areas
for i in xrange(len(area_data)):
    kw_data = {}
    for col in area_data.columns:
        kw_data.setdefault(col, area_data.iloc[i][col])
    if t_sh_industry_areas.find_one(kw_data) == None:
        id = t_sh_industry_areas.insert_one(kw_data).inserted_id
    
class_data = pd.read_csv("./data/platform_company/industry_class.csv")
db = client.holmesdb
t_sh_industry_class = db.t_sh_industry_class
for i in xrange(len(class_data)):
    kw_data = {}
    for col in class_data.columns:
        kw_data.setdefault(col, class_data.iloc[i][col])
    if t_sh_industry_class.find_one(kw_data) == None:
        id = t_sh_industry_class.insert_one(kw_data).inserted_id

interest_data = pd.read_csv("./data/platform_company/industry_interest.csv")
db = client.holmesdb
t_sh_industry_interest = db.t_sh_industry_interest
for i in xrange(len(interest_data)):
    kw_data = {}
    for col in interest_data.columns:
        kw_data.setdefault(col, interest_data.iloc[i][col])
    if t_sh_industry_interest.find_one(kw_data) == None:
        id = t_sh_industry_interest.insert_one(kw_data).inserted_id