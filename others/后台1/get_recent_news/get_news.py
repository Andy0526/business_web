# coding=utf-8
# 获取和讯网上平台信息
import requests
import json
import re
from bs4 import BeautifulSoup


def get_all_id(index):
    data = open('page{}'.format(index), 'r').read()
    name_pattern = re.compile(r"<img alt='(.+?)'")
    id_pattern = re.compile(r"id=(.+?)'")
    result = []
    all_name = name_pattern.findall(data)
    all_id = id_pattern.findall(data)
    for i in range(len(all_name)):
        result.append((all_name[i].decode('utf-8'), all_id[i]))
    return result


def filter_time(string):
    try:
        index = string.index('(')
        return string[:index]
    except:
        return string


def get_news_by_id(id):
    data = requests.get("http://p2p.hexun.com/{}/".format(id))
    data.encoding = 'gbk'
    soup = BeautifulSoup(data.text, "html.parser")
    url_info = []
    url_source = []
    for item in soup.find_all('a'):
        url_info.append((item['href'], item.text))
    for item in soup.find_all('span'):
        url_source.append(item.text)
    result = []
    for i in range(len(url_info)):
        result.append((url_info[i][0], url_info[i][1], filter_time(url_source[0])))

    return result


if __name__ == '__main__':
    result = {}
    for i in range(1, 4):
        for item in get_all_id(i):
            result.setdefault(item[0], [])
            news = get_news_by_id(item[1])
            for each in news:
                result[item[0]].append({'url': each[0], 'title': each[1], 'source': each[2]})
    json.dump(result, open('plat_recent_news.json', 'w'))
