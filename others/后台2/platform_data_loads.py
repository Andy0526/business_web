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
import jieba
import jieba.analyse
import pandas as pd
from pymongo import MongoClient
client=MongoClient()
reload(sys)
sys.setdefaultencoding('utf-8')
csv.field_size_limit(sys.maxint)



def handleContent(string):
    """字符串处理，去标点符号，中文分词，return:unicode"""
    string = string.decode('utf-8')
    #针对自己的文本数据定制化修改
    string = string.replace("<p>", "").replace("</p>", "").replace("<strong>", "").replace("</strong>", "")
    string = string.replace("#r#", "\n").replace("#n#", "\n").replace("", "")
    string = string.replace(" ", "").replace("\n", "").replace("\t", " ")

    string = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！：》，《”。“？、~@#￥%……&*（）]+".decode("utf-8"), "".decode("utf-8"),string)
    string = string.encode('utf-8')
    string = string.translate(None,punctuation+digits+letters+whitespace)
    return string

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




db = client.holmesdb
t_company_info = db.t_company_info
t_company_info.remove()
t_bad_company_info = db.t_bad_company_info
t_bad_company_info.remove()
print "before load all company dadtas", datetime.datetime.now()
def getCompanyList():
    company_dict = {}
    company_f_in = csv.reader(file(u"data/platform_company/网贷之家.csv", "r"))
    lines = [line for line in company_f_in]
    for line in lines[1:]:
        company_dict.setdefault(line[1], 0)
    company_f_in = csv.reader(file(u"data/platform_company/融360.csv", "r"))
    lines = [line for line in company_f_in]
    for line in lines[1:]:
        company_dict.setdefault(line[0], 0)
    company_f_in = csv.reader(file(u"data/platform_company/百度财富.csv", "r"))
    lines = [line for line in company_f_in]
    for line in lines[1:]:
        company_dict.setdefault(line[1], 0)
    company_f_out = open("data/platform_company/company_list.txt", "w")
    for c in company_dict:
        company_f_out.write(c + "\n")

    all_data_dict = getJsonFile_all('./data/platform_company/wangdai_platform.json')

    #company_f_out = open(r"C:\Python27\Lib\site-packages\jieba-0.37-py2.7.egg\jieba/company_dict.txt", "w")
    company_f_out = open(r"./data/platform_company/company_list.txt", "w")
    for c in company_dict:
        #company_f_out.write(c + " 10000 n\n")
        company_f_out.write(c + "\n")
    return company_dict, all_data_dict

def getBadCompanyList():
    bad_company_dict = {}
    all_data_dict = getJsonFile_all('./data/bad_platform/problem_platform.json')
    return all_data_dict

company_dict, company_info_list = getCompanyList()
company_info_key = company_info_list[0].keys()
bad_company_info_list = getBadCompanyList()
for plat in company_info_list:
    t_company_info.insert(plat)
    if t_company_info.find_one(plat['_id']) == None:
        plat['_id'] =  plat['platName']
bad_company_2015 = []
for plat in bad_company_info_list:
    for company in company_info_list:
        if plat['platform_name'] == company['platName']:
            for key in company:
                if key != 'platName':
                    plat.setdefault(key, company[key])

    plat['_id'] =  plat['platform_name']
    if "online_time" in plat :
        if plat["online_time"].strip().find("年") != -1:
            plat["online_time"] = plat["online_time"].strip()[:4] + ".01"
    if "problem_time" in plat:
         if plat["problem_time"].strip().find("年") != -1:
            plat["problem_time"] = plat["problem_time"].strip()[:4] + ".01"
    if t_bad_company_info.find_one(plat['_id']) == None:
        t_bad_company_info.insert(plat)
    if plat['problem_time'][:4] == '2015':
        bad_company_2015.append(plat)
def writeJsonDict(person, f_out):
    outStr = json.dumps(person, ensure_ascii = False, indent=1)        		 #处理完之后重新转为Json格式
    f_out.write(outStr.encode('utf-8') + '\n')          			         #写回到一个新的Json文件中去
writeJsonDict(bad_company_2015, open("./data/bad_platform/bad_platform_2015.json", "w"))
print "end loads all company datas", datetime.datetime.now()


