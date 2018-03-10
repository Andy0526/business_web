import json

result = {}
plat = json.load(open('platform.json', 'r'))
for item in plat:
    result[item['platName']] = {'term': item['term'],
                                'locationAreaName': item['locationAreaName'],
                                'locationCityName': item['locationCityName'],
                                'onlineDate': item['onlineDate'],
                                'platEarnings': item['platEarnings'],
                                'registeredCapital': item['registeredCapital'],
                                'rank': item['zonghezhishuRanking']
                                }

json.dump(result, open('display_platform.json', 'w'))
