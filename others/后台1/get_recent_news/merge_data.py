import json

data1 = json.load(open('all_plat_recent_news_1.json', 'r'))
data2 = json.load(open('all_plat_recent_news_2.json', 'r'))
data3 = json.load(open('all_plat_recent_news_3.json', 'r'))

result = {}
for item in data1:
    result[item] = data1[item]

for item in data2:
    result[item] = data2[item]

for item in data3:
    result[item] = data3[item]

json.dump(result, open('all_news.json', 'w'))
