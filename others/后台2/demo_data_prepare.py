#encoding=utf8
'''
    __author__ = 'shaohua jiang'
    2016.3.20 19：35 first version
    准备demo数据
'''

import csv
import json
import time
import re
from string import punctuation,digits,letters,whitespace
import os
import datetime
import jieba
import jieba.analyse
import pandas as pd
import sys
from helper import myio
reload(sys)
sys.setdefaultencoding('utf-8')


def getJsonFile(json_fname):
    json_file = file(json_fname, "r")
    json_vector = []
    for line in json_file:
         person_info = json.loads(line)
         json_vector.append(person_info)
    return json_vector

def writeJsonLine(line, f_out):
    line = line.strip().decode('utf-8')
    if line[0] != "{":
        line = line[line.find("{") : ]
    try:
        json_line = json.loads(line)                              	#加载Json文件
    except Exception,e:
        print 'bad line'
        return
    outStr = json.dumps(json_line, ensure_ascii = False)        	#处理完之后重新转为Json格式
    f_out.write(outStr.encode('utf-8') + '\n')          			#写回到一个新的Json文件中去

def writeJsonDict(person, f_out):
    outStr = json.dumps(person, ensure_ascii = False)        		#处理完之后重新转为Json格式
    f_out.write(outStr.encode('utf-8') + '\n')          			#写回到一个新的Json文件中去

# #知识图谱数据
# knowdledge_graph = [
#     {"key_node":"网贷","edge_node":["P2P","互联网金融","债权转让","P2B","高收益","高风险"]},\
#     {"key_node":"陆金所","edge_node":["平安集团","lu.com","上海陆家嘴国际金融资产交易市场股份有限公司","P2P","lufax","董事长 计葵生","稳盈-安业"]}
# ]
# knowdledge_graph_file = open(u"./data/demo_datas/知识图谱.json","w")
# for line in knowdledge_graph:
#     writeJsonDict(line, knowdledge_graph_file)


from pymongo import MongoClient
client=MongoClient()
db = client.holmesdb
t_sh_industry_keywords = db.t_sh_industry_keywords


hot_keywords_file = open(u"./data/demo_datas/热门关键字.json","w")
date_begin = datetime.date(2015, 12, 28)
for i in xrange(1, 0, -1):
    cur_d = date_begin + datetime.timedelta(days=i)
    cur_d_str = datetime.datetime.strftime(cur_d, "%Y-%m-%d")
    res_list = []
    res_dict = {"dt":cur_d_str}
    for res in t_sh_industry_keywords.find({"dt":cur_d_str}):
        if "day_hot_keywords" in res:
            res_dict.setdefault("day_hot_keywords",res["day_hot_keywords"] )
            res_list.append(res["day_hot_keywords"])
        if "week_hot_keywords" in res:
            res_dict.setdefault("week_hot_keywords",res["week_hot_keywords"] )
            res_list.append(res["week_hot_keywords"])
        if "month_hot_keywords" in res:
            res_dict.setdefault("month_hot_keywords",res["month_hot_keywords"] )
            res_list.append(res["month_hot_keywords"])
    if len(res_list) > 1:
        for res in res_list:
           print res
        writeJsonDict(res_dict, hot_keywords_file)

def getArticleBydt(dt, type, quality=0.0):
    table = None
    if type == "news":
        table = db.t_news_di
    elif type == "policy":
        table = db.t_policy_di
    elif type == "expert":
        table = db.t_expert_opinion_di
    elif type == "ugc":
        table = db.t_ugc_di
    res_list = table.find({"item_pub_time":dt})
    res_filter = []
    if type == "ugc":
        for res in res_list:
            content = res["content"]
            if len(content) >= 50:
                res_filter.append(res)
    else:
        for res in res_list:
            source = res["source"]
            content = res["content"]
            if content.find(u"看过本文的人") != -1:
                res["content"] = content[:content.find(u"看过本文的人")]
            if  res["content"].find(u"阅读原文") != -1:
                res["content"] = content[:content.find(u"阅读原文")]
            if  res["content"].find(u"\r\n                    \r\n                        \r\n                        \r\n                        \r\n                        \r\n                            (adsbygoogle = window.adsbygoogle || []).push({});\r\n                        \r\n                    \r\n                    \r\n                    ") != -1:
                res["content"] = content[:content.find(u"\r\n                    \r\n                        \r\n                        \r\n                        \r\n                        \r\n                            (adsbygoogle = window.adsbygoogle || []).push({});\r\n                        \r\n                    \r\n                    \r\n                    ")]
            cnt = 0
            while  res["content"].find("\r\n\r\n") != -1:
                res["content"] = res["content"].replace("\r\n\r\n", "\r\n")
                cnt += 1
            while  res["content"].find("                                            ") != -1:
                res["content"] = res["content"].replace("                                            ", "")
            if len(res["content"]) < 50:
                continue
            res_filter.append(res)
    return res_filter
def getArticleByrangedt(dt_end, day_cnt, type, limit = -1, quality=0.0):
    res_list = []
    date_begin = datetime.date(int(dt_end[:4]), int(dt_end[5:7]), int(dt_end[8:10]))
    for i in xrange(0,  day_cnt):
        cur_d = date_begin + datetime.timedelta(days= -1 * i)
        cur_d_str = datetime.datetime.strftime(cur_d, "%Y-%m-%d")
        res_temp = getArticleBydt(cur_d_str, type)
        for res in res_temp:
            res_list.append(res)
    if limit == -1:
        return res_list
    else:
        return res_list[:limit]
news_res = getArticleByrangedt("2015-12-29", 30, "news", 1000)
myio.writeJsonDict(news_res,  open(u"./data/demo_datas/新闻.json","w"), "rows")
news_res = getArticleByrangedt("2015-12-28", 30, "policy", 1000)
myio.writeJsonDict(news_res,  open(u"./data/demo_datas/政策.json","w"), "rows")
news_res = getArticleByrangedt("2015-12-28", 30,  "expert", 1000)
myio.writeJsonDict(news_res,  open(u"./data/demo_datas/专家观点.json","w"), "rows")
# news_res = getArticleByrangedt("2015-12-28", 30,  "ugc", 1000)
# myio.writeJsonDict(news_res,  open(u"./data/demo_datas/用户评论.json","w"), "rows")
# #热门事件数据
# hot_event_graph = [
#     {"event":"e租宝涉嫌违法经营分崩离析","details":"12月8日，ｅ租宝网站以及关联公司在开展互联网金融业务中涉嫌违法经营活动，正接受有关部门调查。"},\
#     {"event":"宜人贷上市","details":"宜人贷纽交所挂牌成P2P网贷上市第一股"},
#     {"event":"P2P网贷成交额首破万亿","details":"第一网贷发布《2015年1-11月全国P2P网贷行业快报》"},
#     {"event":"指导意见发布","details":"等十部委发布《关于促进互联网金融健康发展的指导意见》"}
# ]
# hot_event_graph_file = open(u"./data/demo_datas/热门事件.json","w")
# for line in hot_event_graph:
#     writeJsonDict(line, hot_event_graph_file)


# #平台数据汇总
# data1 = pd.read_csv(u"data/platform_company/网贷之家.csv")
# data2 = pd.read_csv(u"data/platform_company/融360.csv")
# companty_info_file = open(u"./data/demo_datas/平台数据.json","w")
# columns = ["平台","评级","平均收益","上线时间","平台背景","人气指数","成交量","平均利率","平均借款期限","累计待还金额"]
# company_dict = {}
# for i in data1.index:
#     name = data1.iloc[i]["平台"]
#     for col in columns:
#         if col in data1.iloc[i]:
#             company_dict.setdefault(name, {}).setdefault(col, data1.iloc[i][col])
# for i in data2.index:
#     name = data2.iloc[i]["平台"]
#     for col in columns:
#         if col in data2.iloc[i]:
#             company_dict.setdefault(name, {}).setdefault(col, data2.iloc[i][col])
# for com in company_dict:
#     com_info = company_dict[com]
#     for col in columns:
#         if col not in com_info:
#             com_info.setdefault(col, "")
#     outStr = json.dumps(com_info, ensure_ascii = False)        		#处理完之后重新转为Json格式
#     companty_info_file.write(outStr.encode("utf-8") + '\n')          			#写回到一个新的Json文件中去
