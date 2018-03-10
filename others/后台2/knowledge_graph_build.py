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
import helper.textprocessing as tp
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
    institute_dict = {}
    location_dict = {}
    people_dict = {}

    row_cnt = 0
    for res in res_list:
        row_cnt += 1
        # if row_cnt >= 2000: break
        title = res["title"]
        content = res["content"]
        doc = myio.handleContent(title) + " " + myio.handleContent(content)
        words = pseg.cut(doc)
        for (word, flag) in words:
            if flag.find("n") != -1:
                if len(word) == 1:
                    continue
                word1 = word[0].encode("utf-8")
                word2 = word[:2].encode("utf-8")
                if word1 in last_name_dict or word2 in last_name_dict:
                    #print word[0], word[:2]
                    people_dict[word] = people_dict.setdefault(word, 0) + 1
                if flag.find("t") != -1 or flag.find("r") != -1:
                    institute_dict[word] = institute_dict.setdefault(word, 0) + 1
                if  flag.find("s") != -1:
                    location_dict[word] = location_dict.setdefault(word, 0) + 1
                #print w.word, w.flag
                ntoken_dict[word] = ntoken_dict.setdefault(word, 0) + 1
    ntoken_list = sorted(ntoken_dict.items(), lambda a, b: -cmp(a[1], b[1]))
    people_list = sorted(people_dict.items(), lambda a, b: -cmp(a[1], b[1]))
    institute_list = sorted(institute_dict.items(), lambda a, b: -cmp(a[1], b[1]))
    location_list = sorted(location_dict.items(), lambda a, b: -cmp(a[1], b[1]))

    f_ntoken = open(knowledge_graph_dir + "news_ntoken.txt", "w")
    f_peo = open(knowledge_graph_dir + "news_people.txt", "w")
    f_ins = open(knowledge_graph_dir + "news_institute.txt", "w")
    f_loc = open(knowledge_graph_dir + "news_location.txt", "w")
    for (word, freq) in ntoken_list:
        print word, freq
        f_ntoken.write("%s\n"%word)
    for (word, freq) in institute_list:
        print word, freq
        f_ins.write("%s\n"%word)
    for (word, freq) in location_list:
        print word, freq
        f_loc.write("%s\n"%word)
    for (word, freq) in people_list:
        print word, freq
        f_peo.write("%s\n"%word)

def extractRelation():
    db = client.holmesdb
    t_news = db.t_news_di
    res_list = t_news.find()

    pair3_dict = {}
    pair2_dict = {}
    row_cnt = 0
    for res in res_list:
        row_cnt += 1
        if row_cnt >= 20000: break
        title = res["title"]
        if title.find(u"要不要打破刚性兑付？") != -1:
            continue
        content = res["content"]
        content_sen = tp.cut_sentence_2(content)
        sentence_list = [title] + content_sen
        for sen in sentence_list:
            sen = myio.handleContent(sen)
            if len(sen) < 5: continue
            if sen.find(u"尹许尹") != -1:
                print title
                print content
                print sen
            words = pseg.cut(sen)
            ntoken_list = []
            for (word, flag) in words:
                if flag.find("n") != -1 and (flag.find("r") != -1 or flag.find("s") != -1 or flag.find("t") != -1):
                    ntoken_list.append(word)
            for i in xrange(len(ntoken_list) - 1):
                for j in xrange(i+1, len(ntoken_list)):
                    if ntoken_list[i] == ntoken_list[j]:
                        continue
                    pair2 = (ntoken_list[i], ntoken_list[j])
                    pair2_dict[pair2] = pair2_dict.setdefault(pair2, 0) + 1
                    for k in xrange(j+1, len(ntoken_list)):
                        if ntoken_list[i] == ntoken_list[k] or ntoken_list[j] == ntoken_list[k]:
                            continue
                        pair3 = (ntoken_list[i], ntoken_list[j], ntoken_list[k])
                        pair3_dict[pair3] = pair3_dict.setdefault(pair3, 0) + 1
    pair2_list = sorted(pair2_dict.items(), lambda a,b: -cmp(a[1], b[1]))
    # for (w1, w2) in pair2_list:
    #     print w1[0], w1[1],  w2
    pair3_list = sorted(pair3_dict.items(), lambda a,b: -cmp(a[1], b[1]))
    # for (w1, w2) in pair3_list:
    #     print w1[0], w1[1], w1[2], w2
    f_rel = open(knowledge_graph_dir + "news_relation.txt", "w")
    for (w1, w2) in pair2_list[:500000]:
        f_rel.write("%s %s\n"%(w1[0], w1[1]))
    for (w1, w2) in pair3_list[:3000000]:
        f_rel.write("%s %s %s\n"%(w1[0], w1[1], w1[2]))

if __name__ == "__main__":
    # pipeline step1
    # extractEntity()
    # pipeline step3
    extractRelation()