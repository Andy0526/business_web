#encoding=utf8
'''
    __author__ = 'Administrator'
    2016.4.16 19:50 first version
    处理互联网金融协会名单
'''
import csv
import os
import sys
import bs4
import datetime
import requests, html2text
reload(sys)
sys.setdefaultencoding('utf-8')

f_in = open(u"../data/knowledge_graph/中国互联网金融协会会员名单.txt")
f_out = open(u"../data/knowledge_graph/中国互联网金融协会会员名单_分开.txt", "w")
f_relation_out = open(r"../data/knowledge_graph/relation_equal.txt", "w")

for line in f_in:
    print line.strip()
    if line.find( u"）") == -1:
        f_out.write(line)
    else:
        line_rep = line.strip().replace(u"）", "#").replace(u"（", "$")
        print "\t", line_rep
        if line_rep[-1] == "#":
            rev_index = line_rep.rfind("$")
            rev_end_index = line_rep.rfind("#")
            pname1 = line_rep[:rev_index]
            pname2 = line_rep[rev_index+1:-1]
            print "\t", pname1, pname2
            pname1 = pname1.replace("#", u"）").replace("$", u"（")
            f_out.write(pname1 + "\n")
            f_out.write(pname2 + "\n")
            f_relation_out.write("%s,%s"%(pname1, pname2))
            f_relation_out.write("%s,%s"%(pname2, pname1))
        else:
            f_out.write(line)

