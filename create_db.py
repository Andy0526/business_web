# -*- coding: utf-8 -*-
import sqlite3
import csv

import  json
def insert_news_type(news_type):
    conn = sqlite3.connect('static/data/p2p.db')
    print "Opened database successfully"

    reader = csv.reader(file('static/data/' + news_type + '.csv', 'rb'))
    for line in reader:
        if reader.line_num == 1:
            continue
        news_data = (line[0], line[2], line[3], line[4], line[5], line[6], line[7])

        conn.executemany(
           "INSERT INTO "+news_type+"(item_id,source,url,author,title,content,item_pub_time) VALUES (?,?,?,?,?,?,?)", news_data)
        conn.commit()
    print "Records created successfully";
    conn.close()

#insert_news_type("news")

#news_json = json.load(open('static/data/hot_topic/1/news.json', 'r'))
#print type(news_json['item_list'])



def detail_platforms():
    platforms_json = json.load(open('static/data/platform_info.json','r'))

    platforms = []
    for platform_name in platforms_json:
         platform_dict =  platforms_json[platform_name];
         platform_dict['platform_name'] = platform_name;
         print platform_dict

#detail_platforms()

recent_reviews_json = json.load(open('static/data/comments_data.json','r'))
print recent_reviews_json[u'投哪网']