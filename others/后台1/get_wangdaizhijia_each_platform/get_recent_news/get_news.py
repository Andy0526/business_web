import requests
import json
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'

}

result = {}


def get_news(pinyin):
    temp = []
    req = requests.get('http://www.wdzj.com/dangan/{}/'.format(pinyin), headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "html.parser")
    try:
        for item in soup.find_all('ul', attrs={'class': "newsList"}):
            for each in item.find_all('a'):
                if 'http' in each['href']:
                    the_url = each['href']
                else:
                    the_url = 'www.wdzj.com' + each['href']
                temp.append({'url': the_url, 'title': each.text})

        return temp
    except:
        return temp


for item in json.load(open('platform_search.json', 'r')):
    print item['platName']
    result[item['platName']] = get_news(item['platPin'])

json.dump(result, open('all_plat_wangdai_news.json', 'w'))
