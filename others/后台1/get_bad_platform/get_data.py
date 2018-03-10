import requests
from bs4 import BeautifulSoup
import json

data = requests.get("http://shuju.wdzj.com/problem-1.html", "html.parser").text
soup = BeautifulSoup(data, "html.parser")
all_data = soup.find_all("tr", attrs={"class": ""})
result = []
for item in all_data[1:]:
    raw = item.text.strip().split('\n')
    result.append({"index": raw[0], "platform_name": raw[1], "problem_time": raw[2], "online_time": raw[3],
                   "registration capital": raw[4], "region": raw[5], "money": raw[6], "number": raw[7],
                   "event_type": raw[8]})
all_data2 = soup.find_all("tr", attrs={"class": "tb_bg_gray"})
for item in all_data2:
    raw = item.text.strip().split('\n')
    result.append({"index": raw[0], "platform_name": raw[1], "problem_time": raw[2], "online_time": raw[3],
                   "registration capital": raw[4], "region": raw[5], "money": raw[6], "number": raw[7],
                   "event_type": raw[8]})


def toint(str):
    return int(str.replace(",", ""))


result.sort(key=lambda x: toint(x['index']))
json.dump(result, open('problem_platform.json', 'w'))
