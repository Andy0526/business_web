import requests
import json

url = 'http://shuju.wdzj.com/wdzj-archives-chart.html?wdzjPlatId={}&type={}&status=0'

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Host': 'www.wdzj.com',
    'origin': 'http://www.wdzj.com',
    'Referer': 'http://www.wdzj.com/dangan/tdw/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'

}

result = {}

plat = json.load(open('platform_info.json', 'r'))
index = 0
for each in plat:
    try:
        print index
        theid = each['platId']
        result[theid] = {}
        type0 = requests.get(url.format(theid, 0)).json()
        type1 = requests.get(url.format(theid, 1)).json()
        type2 = requests.get(url.format(theid, 3)).json()
        result[theid]['0'] = {'x': type0['x'], 'y1': type0['y1'], 'y2': type0['y2']}
        result[theid]['1'] = {'x': type1['x'], 'y1': type1['y1'], 'y2': type1['y2']}
        result[theid]['2'] = {'x': type2['x'], 'y1': type2['y1'], 'y2': type2['y2']}
        index += 1
    except:
        continue
json.dump(result, open('platform_chart.json', 'w'))
