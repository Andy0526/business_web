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
from pymongo import MongoClient
client=MongoClient()
db = client.holmesdb



def insertDB(mongodb_table, line, columns):
    try:
        ori = columns[0]
        columns[0] = "_id"
        data = {}
        for i in xrange(0, len(columns)):
            data.setdefault(columns[i], line[i])
        mongodb_table.insert(data)
        columns[0] = ori
    except Exception :
         columns[0] = ori
         print Exception
         return

