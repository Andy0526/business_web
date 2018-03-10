import json

data = json.load(open('../platform_chart.json', 'r'))

name_id = {}

for item in json.load(open('platform_info.json')):
    name_id[item['platName']] = item['platId']

result = {}

for item in json.load(open('display_platform.json', 'r')):
    result[item] = data[name_id[item]]

json.dump(result, open('platform_chart.json', 'w'))
