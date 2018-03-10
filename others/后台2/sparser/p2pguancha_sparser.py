# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 21:25:37 2016

@author: yue
"""

import requests
import json
import time

idd = '1991'
while(True):
    url = "http://www.p2pguancha.com/api.php?action=categorycontent&cid=11&id="+idd+"&num=10"
    r = requests.get(url)
    result = r.json()
    for i in range(0,len(result['article'])):
        print result['article'][i].keys()
        save = {}
        save['source '] = "P2P观察网"
        save['item_id'] = "p2pgc_" + result['article'][i]['id'].encode('utf8')
        save['item_type'] = "news"
        save['author'] = "" if "author_id" in result['article'][i] else  result['article'][i]['author_id'].encode('utf8')
        save['tags'] =  result['article'][i]['tag_name'].encode('utf8')
        save['title'] = result['article'][i]['title'].encode('utf8')
        save['content'] = result['article'][i]['content'].encode('utf8')
        save['url'] = "http://www.p2pguancha.com/article/"+save['item_id']+".html"
        save['source_name'] = result['article'][i]['source_name'].encode('utf8')
        save['news_pub_time'] = result['article'][i]['release_time'].encode('utf8')
        save['gmt_create'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        save_str = json.dumps(save,ensure_ascii=False)
        f = open("p2pguancha_news.txt",'a')
        f.write(save_str+'\n')
        f.close()      
        idd = save['item_id']
        print idd