import json

data = json.load(open('display_platform_detail.json', 'r'))

temp = []
for item in data:
    temp.append([data[item]['zonghezhishu'], item])

temp.sort(reverse=True)
for i in enumerate(temp, 1):
    data[i[1][1]]['zonghezhishuRanking'] = i[0]

json.dump(data, open('result.json', 'w'))
