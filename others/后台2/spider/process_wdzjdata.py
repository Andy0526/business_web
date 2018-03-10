#encoding=utf8
'''
    __author__ = 'Administrator'
    2016.3.6 16:26 first version
    处理从网贷之家爬取来的数据，tab改‘,’，并附加dt字段
'''


import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import datetime

d1 = '2016-03-15'
f_in_area = open("../data/platform_company/platform_areas.txt")
f_out_area = open("../data/platform_company/platform_areas_our.csv", "w")
area_data = [line[:-1] for line in f_in_area]
columns = area_data[0]
f_out_area.write(columns + ",dt\n")
for line in area_data[1:]:
    if len(line) <= 2:
        d1 =  datetime.datetime.strptime(d1, "%Y-%m-%d")
        d1 = d1 - datetime.timedelta(days=31)
        d1 = datetime.datetime.strftime(d1, "%Y-%m-%d")
    else:
        f_out_area.write(line + "," + d1[:7] + "-01" +"\n")



d1 = '2016-03-15'
f_in_area = open("../data/platform_company/platform_class.txt")
f_out_area = open("../data/platform_company/platform_class_our.csv", "w")
area_data = [line[:-1] for line in f_in_area]
columns = area_data[0]
f_out_area.write(columns + ",dt\n")
for line in area_data[1:]:
    if len(line) <= 2:
        d1 =  datetime.datetime.strptime(d1, "%Y-%m-%d")
        d1 = d1 - datetime.timedelta(days=31)
        d1 = datetime.datetime.strftime(d1, "%Y-%m-%d")
    else:
        f_out_area.write(line + "," + d1[:7] + "-01" +"\n")