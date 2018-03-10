#encoding=utf8
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


def writeJsonDict(person, f_out):
    outStr = json.dumps(person, ensure_ascii = False)        		#处理完之后重新转为Json格式
    f_out.write(outStr.encode('utf-8') + '\n')          			#写回到一个新的Json文件中去

def writeJsonDict(person, f_out, row_type=None):
    row_flag = 1 if row_type == "rows" else None
    outStr = json.dumps(person, ensure_ascii = False, indent=row_flag)        		 #处理完之后重新转为Json格式
    f_out.write(outStr.encode('utf-8') + '\n')          			                 #写回到一个新的Json文件中去

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
