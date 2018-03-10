# coding=utf-8
import json

data = json.load(open('data_2.json', 'r'))
result = {}
for item in data:
    result[item] = []
    for each in data[item]:
        temp = []
        if each['url'] not in temp and len(each['title']) > 1:
            result[item].append({'url': each['url'], 'title': each['title']})
        else:
            continue

json.dump(result, open('data_3.json', 'w'))
