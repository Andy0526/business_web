#encoding=utf8
'''
    __author__ = 'Administrator'
    2016.4.2 14:11 first version
    问题平台分析
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
import types
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

print "before load bad company datas", datetime.datetime.now()
db = client.holmesdb
t_news = db.t_news_di
t_policy = db.t_policy_di
t_ugc = db.t_ugc_di
t_expert = db.t_expert_opinion_di
t_news_caixin = db.t_news_caixin_di
news_res = t_news.find()
policy_res = t_policy.find()
ugc_res = t_ugc.find()
expert_res = t_expert.find()

bad_company_2015 = getJsonFile_all("./data/bad_platform/bad_platform_2015.json")
print "end load bad company datas", datetime.datetime.now()


print "before analyze bad company datas", datetime.datetime.now()
def getColumnDict(bad_company_2015, column):
    statistic_dict = {}
    for plat in bad_company_2015:
        if type(plat[column]) is types.StringType:
            value = plat[column].strip()
        elif type(plat[column]) is types.FloatType:
            value = plat[column]
        elif type(plat[column]) is types.IntType:
            value = plat[column]
        else:
            value = plat[column]
        statistic_dict[value] = statistic_dict.setdefault(value, 0) + 1
    return statistic_dict
prob_month_statistic = getColumnDict(bad_company_2015, "problem_time")
region_statistic = getColumnDict(bad_company_2015, "region")
event_type_statistic = getColumnDict(bad_company_2015, "event_type")
online_time_statistic = getColumnDict(bad_company_2015, "online_time")
registmoney_statistic = {}
registmoney_statistic2 = {}
run_time_statistic = {}
for plat in bad_company_2015:
    online_time = plat["online_time"].strip()
    prob_month = plat["problem_time"].strip()
    if online_time == "-":
        online_time = "2013.01"
    y1, m1 = int(online_time[:4]), int(online_time[5:])
    y2, m2 = int(prob_month[:4]), int(prob_month[5:])
    delta = (y2 - y1) * 12 + m2  - m1
    #print y1, m1, y2, m2, delta
    run_time_statistic[delta] = run_time_statistic.setdefault(delta, 0) + 1

    regist = plat["registration capital"]
    regist_str = ""
    if regist.find(".") != -1:
        regist = int(regist[:regist.find(".")])
        if regist >= 100 and regist <= 500:
            regist_str = "100~500"
        elif regist > 500 and regist <= 999:
            regist_str = "500~999"
        elif regist > 999 and regist <= 1000:
            regist_str = "1000"
        elif regist > 1000 and regist <= 2000:
            regist_str = "1001~2000"
        elif regist > 2000 and regist <= 4999:
            regist_str = "2000~4999"
        elif regist > 4999 and regist <= 9999:
            regist_str = "5000~9999"
        else:
            regist_str = "10000以上"
    else:
        regist = -1
        regist_str = "未知"
    registmoney_statistic[regist] = registmoney_statistic.setdefault(regist, 0) + 1
    registmoney_statistic2[regist_str] = registmoney_statistic2.setdefault(regist_str, 0) + 1
# for month in prob_month_statistic:
#     print month, prob_month_statistic[month]
# for region in region_statistic:
#     print region, region_statistic[region]
# for event_type in event_type_statistic:
#     print event_type, event_type_statistic[event_type]
# for delta in run_time_statistic:
#     print delta, run_time_statistic[delta]
# print registmoney_statistic2
# print sorted(registmoney_statistic.items(), lambda a, b: -cmp(a[1], b[1]))
article_res = [news_res, policy_res, ugc_res, expert_res]
key = ["news", "policy", "ugc", "expert"]
month_summary = {}
for i in xrange(4):
    for res in article_res[i]:
        if res['item_pub_time'] >= '2015-01-01' and res['item_pub_time'] <= '2015-12-31':
            title = res['title']
            content = res['content']
            t = res['item_pub_time']
            m = t[5:7]
            date = t[5:].replace("-", ".").split(" ")[0]
            # if content.find("e租宝") != -1 or content.find("E租宝") != -1:
            #     month_summary[m] = month_summary.setdefault(m, 0) + 1
            #     print m,  month_summary[m]
            if content.find(u"云融通") != -1:
                month_summary[m] = month_summary.setdefault(m, 0) + 1
                print m,  month_summary[m]
print month_summary
print "end analyze bad company datas", datetime.datetime.now()


def writeJsonDict(person, f_out):
    outStr = json.dumps(person, ensure_ascii = False)        		#处理完之后重新转为Json格式
    f_out.write(outStr.encode('utf-8') + '\n')          			#写回到一个新的Json文件中去
print "begin save datas", datetime.datetime.now()
writeJsonDict(prob_month_statistic, open("./data/bad_platform/bad_platform_prob_month_statistic.json", "w"))
writeJsonDict(region_statistic, open("./data/bad_platform/bad_platform_region_statistic.json", "w"))
writeJsonDict(event_type_statistic, open("./data/bad_platform/bad_platform_event_type_statistic.json", "w"))
writeJsonDict(run_time_statistic, open("./data/bad_platform/bad_platform_runtime_statistic.json", "w"))
writeJsonDict(registmoney_statistic2, open("./data/bad_platform/bad_platform_registmoney_statistic.json", "w"))
print "end save datas", datetime.datetime.now()