import requests
import json
from bs4 import BeautifulSoup

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
}


def get_result(platurl):
    data = {
        'ht': 1,
        'h': platurl
    }
    result = []
    try:
        html = requests.get('http://tool.chinaz.com/history/', data=data, headers=header).text
        soup = BeautifulSoup(html, "html.parser")
        info = soup.find_all('ul', attrs={'class': 'ResultListWrap'})[0]
        # text = [item.strip() for item in info.text.strip().split('\n') if item.strip()]


        for item in info.find_all('li', attrs={'class': 'ReListCent ReLists clearfix'}):
            temp = []
            for each in item.find_all('div'):
                if each.text.strip() != '':
                    temp.append(each.text.strip())
            if len(temp) > 9:
                continue
            if len(temp) < 9:
                while len(temp) != 9:
                    temp.append('--')
            temp2 = []
            for each in temp:
                if each.startswith('arguments'):
                    temp2.append('--')
                else:
                    temp2.append(each)
            result.append(temp2)
        for item in info.find_all('li', attrs={'class': 'ReListCent ReLists clearfix bg-list'}):
            temp = []
            for each in item.find_all('div'):
                if each.text.strip() != '':
                    temp.append(each.text.strip())
            if len(temp) > 9:
                continue
            if len(temp) < 9:
                while len(temp) != 9:
                    temp.append('--')
            temp2 = []
            for each in temp:
                if each.startswith('arguments'):
                    temp2.append('--')
                else:
                    temp2.append(each)
            result.append(temp2)
        return result
    except Exception, e:
        print e
        return result


def change_url(url):
    temp = url.split('//')
    if temp[1][-1] == '/':
        return temp[1][:-1]
    else:
        return temp[1]


all_platform = json.load(open('platform_basic.json', 'r'))
all_result = {}
for each in all_platform:
    try:
        print each['platName']
        all_result[each['platName']] = []
        result = get_result(change_url(each['platUrl']))
        result.sort()
        all_result[each['platName']].extend(result)
    except Exception, e:
        print e
        continue

json.dump(all_result, open('result.json', 'w'))
