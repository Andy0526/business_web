import json

new_result = []
data = json.load(open('all_plat.json', 'r'))

for item in data:
    temp = {}
    temp['allPlatNamePin'] = item['allPlatNamePin']
    temp['locationAreaName'] = item['locationAreaName']
    temp['locationCityName'] = item['locationCityName']
    temp['onlineDate'] = item['onlineDate']
    temp['platEarnings'] = item['platEarnings']
    temp['platLogoUrl'] = item['platLogoUrl']
    temp['platName'] = item['platName']
    temp['platUrl'] = item['platUrl']
    temp['registeredCapital'] = item['registeredCapital']
    temp['term'] = item['term']
    temp['zonghezhishu'] = item['zonghezhishu']
    temp['zonghezhishuRanking'] = item['zonghezhishuRanking']
    temp['platStatus'] = item['platStatus']
    new_result.append(temp)
json.dump(new_result, open('platform_basic.json', 'w'))
