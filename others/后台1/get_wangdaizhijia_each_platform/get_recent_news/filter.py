import json

data = json.load(open('all_plat_wangdai_news.json', 'r'))
for each in data:
    for item in data[each]:
        if not item['url'].startswith('http'):
            item['url'] = 'http://' + item['url']

json.dump(data, open('all_plat_related_news.json', 'w'))
