import requests
import json

url = 'http://www.wdzj.com/wdzj/html/json/dangan_search.json'

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Host': 'www.wdzj.com',
    'Referer': 'http://www.wdzj.com/dangan/tdw/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'

}

data = requests.get(url, headers=headers).json()
json.dump(data, open('platform_search.json', 'w'))
