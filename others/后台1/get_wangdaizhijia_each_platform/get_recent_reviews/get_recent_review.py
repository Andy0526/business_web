import requests
import json

header = {
    'Accept': '*/*',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'www.wdzj.com',
    'Origin': 'http://www.wdzj.com',
    'Referer': 'http://www.wdzj.com/dangan/dianping/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'

}

result = []
for i in range(1, 10):
    data = {
        'orderType': 0,
        'currentPage': i,
        'allReview': 1
    }
    data = \
        requests.post('http://www.wdzj.com/front_plat-review-list', headers=header, data=data).json()[0]['platReview'][
            'reviewList']
    result.extend(data)
json.dump(result, open('raw_recent_reviews.json', 'w'))
