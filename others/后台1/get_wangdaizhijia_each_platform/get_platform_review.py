import requests
import json

url = 'http://www.wdzj.com/front_plat-review-list'

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Host': 'www.wdzj.com',
    'origin': 'http://www.wdzj.com',
    'Referer': 'http://www.wdzj.com/dangan/tdw/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'

}

result = {}

plat = json.load(open('platform_search.json', 'r'))
index = 0
for each in plat:
    try:
        print index
        result[each['platId']] = {}
        review = requests.post(url, headers=headers, data={'platId': each['platId']}).json()[0]['platReview']
        rowCount = review['rowCount']
        pagecount = review['pageCount']
        result[each['platId']]['rowCount'] = rowCount
        result[each['platId']]['reviews'] = []
        for page in range(pagecount):
            data = {
                'platId': each['platId'],
                'currentPage': page + 1
            }
            reviews = requests.post(url, headers=headers, data=data).json()[0]['platReview']['reviewList']
            result[each['platId']]['reviews'].extend(reviews)
        index += 1
    except Exception, e:
        print e
        index += 1
        continue

json.dump(result, open('platform_reviews.json', 'w'))
