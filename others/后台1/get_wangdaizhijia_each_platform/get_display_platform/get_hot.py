import requests
import json

url = 'http://www.wdzj.com/front_select-plat'
header = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'www.wdzj.com',
    'Origin': 'http://www.wdzj.com',
    'Referer': 'http://www.wdzj.com/dangan/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
}
result = []
for i in range(1, 5):
    print i
    para = {
        'params': '',
        'sort': 'grade',
        'currPage': i
    }
    result.extend(requests.post(url, headers=header, data=para).json()['list'])
json.dump(result, open('platform.json', 'w'))
