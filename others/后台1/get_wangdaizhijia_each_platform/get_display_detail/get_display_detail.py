import json

all_plat = json.load(open('all_plat.json', 'r'))
# display_plat = json.load(open('../get_display_platform/display_platform.json'))
result = {}
#
for item in all_plat:
    temp = {}
    temp['allPlatNamePin'] = item['allPlatNamePin']
    temp['locationAreaName'] = item['locationAreaName']
    temp['locationCityName'] = item['locationCityName']
    temp['onlineDate'] = item['onlineDate']
    temp['platEarnings'] = item['platEarnings']
    temp['platLogoUrl'] = item['platLogoUrl']
    temp['platUrl'] = item['platUrl']
    temp['registeredCapital'] = item['registeredCapital']
    temp['term'] = item['term']
    temp['zonghezhishu'] = item['zonghezhishu']
    temp['zonghezhishuRanking'] = item['zonghezhishuRanking']
    temp['platStatus'] = item['platStatus']
    result[item['platName']] = temp

json.dump(result, open('all_platform_basic.json', 'w'))
