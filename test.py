# -*- coding: utf-8 -*-
import csv
import sys
csv.field_size_limit(sys.maxsize)


def info_news_detail(news_id):
    reader = csv.reader(file('static/data/news.csv', 'rb'))
    for line in reader:
        if reader.line_num == 1:
            continue
        if news_id == line[0]:
            print "success"
            news_item = dict()
            news_item['type'] = 'news'
            news_item['item_id'] = line[0]
            news_item['url'] = line[3]
            news_item['author'] = line[4]
            news_item['title'] = line[5]
            news_item['content'] = line[6]
            news_item['item_pub_time'] = line[7]
            print news_item['content']
            return news_item


info_news_detail("77");


