 #encoding=utf8
'''
    __author__ = 'Administrator'
    2016.3.31测试
'''
import sys
import os
import json
reload(sys)
sys.setdefaultencoding('utf-8')


def getJsonFile_all(json_fname):
    json_file = open(json_fname, "r")
    dict = json.load(json_file)
    json_file.close()
    return dict
def writeJsonDict(person, f_out):
    outStr = json.dumps(person, ensure_ascii = False)        		#处理完之后重新转为Json格式
    f_out.write(outStr.encode('utf-8') + '\n')          			#写回到一个新的Json文件中去


# json_list = []
# for cur, dir, fname_list in os.walk("./data/_temp"):
#     for f in  fname_list:
#         print f
#         if f[0] == 'a':
#             continue
#         f_path =  os.path.join(cur, f)
#         json_data = getJsonFile_all(f_path)
#         date_dict = {}
#         for data in json_data:
#             d = data["item_pub_time"].split(" ")[0].replace("-", ".")
#             date_dict[d] = date_dict.setdefault(d, 0) + 1
#         print sorted(date_dict.items(), lambda a,b: cmp(a[0], b[0]))
#         new_path = os.path.join(cur, "ana_" + f)
#         writeJsonDict(date_dict, open(new_path, "w"))


#encoding=utf8
'''
    __author__ = 'Administrator'
    2016.4.17 01:08 first version
    构建知识图谱，pipeline
    1、词性标注
    2、歧义消除
    3、关系抽取
    4、知识推理
    5、知识表示
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
import jieba.posseg as pseg
import math
import pandas as pd
from gensim import corpora,models
from helper.textprocessing import handleContent
from pymongo import MongoClient
client=MongoClient()
reload(sys)
sys.setdefaultencoding('utf-8')

knowledge_graph_dir = "./data/knowledge_graph/"
def getLastNameDict():
    last_name_dict ={}
    name_vec = [line.strip().split(" ") for line in open(knowledge_graph_dir + u"中国姓.txt")]
    for vec in name_vec:
        if len(vec) > 1:
            for v in vec:
                last_name_dict.setdefault(v, 0)
    return last_name_dict

def extractEntity():
    db = client.holmesdb
    t_news = db.t_news_di
    res_list = t_news.find()
    last_name_dict = getLastNameDict()

    ntoken_dict = {}
    people_dict = {}
    row_cnt = 0
    for res in res_list:
        row_cnt += 1
        title = res["title"]
        content = res["content"]
        doc = myio.handleContent(title) + " " + myio.handleContent(content)
        words = pseg.cut(doc)
        for (word, flag) in words:
            if flag.find("n") != -1:
                print word, flag
                word1 = word[0].encode("utf-8")
                word2 = word[:2].encode("utf-8")
                if word1 in last_name_dict or word2 in last_name_dict:
                    #print word[0], word[:2]
                    people_dict[word] = people_dict.setdefault(word, 0) + 1
                else:
                #print w.word, w.flag
                   ntoken_dict[word] = ntoken_dict.setdefault(word, 0) + 1
    ntoken_list = sorted(ntoken_dict.items(), lambda a, b: -cmp(a[1], b[1]))
    people_list = sorted(people_dict.items(), lambda a, b: -cmp(a[1], b[1]))


if __name__ == "__main__":
    #pipeline step1
    extractEntity()