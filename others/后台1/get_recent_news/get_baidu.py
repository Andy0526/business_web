# coding=utf-8
# 抓取相关百度新闻
import requests
from bs4 import BeautifulSoup
import urllib
import json

result = {}


def get_news(word):
    name = urllib.urlencode({'name': word}).split('=')[1]
    soup = BeautifulSoup(
        requests.get(
            'http://www.baidu.com/s?tn=baidurt&rtt=1&bsst=1&cl=3&ie=utf-8&bs={}&f=8&rsv_bp=1&wd={}&inputT=0'.format(
                name,
                name)).text,
        "html.parser"
    )
    for item in soup.find_all('a', attrs={'target': '_blank'}):
        if item[
            'href'] != '#' and item.text != u'百度快照' and item.text != u'注册' \
                and u'去网页搜索' not in item.text and item.text != u'帮助' and item.text != '':
            yield {'url': item['href'], 'title': item.text.strip()}


all_plat = json.load(open('platform_basic.json', 'r'))[2500:2500]


def get_plat_name():
    for item in all_plat:
        result.setdefault(item['platName'], [])
        print item['platName']
        for each in get_news(item['platName'].encode('utf-8')):
            result[item['platName']].append(each)


if __name__ == '__main__':
    get_plat_name()
    json.dump(result, open('all_plat_recent_news_3.json', 'w'))
