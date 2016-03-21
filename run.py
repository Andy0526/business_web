# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
import json
import csv
import sys
csv.field_size_limit(sys.maxsize)

app = Flask(__name__)


# 主页
@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")


# 新闻 >> 热点
@app.route('/info/hot', methods=['GET'])
def info_hot():
    platforms_json = json.load(open('static/data/hot_keyword.json', 'r'))
    max_num = 40

    num = 0
    day_hot_keywords = []
    for day_hot_keyword_str in platforms_json['day_hot_keywords'].split(';'):
        day_hot_keyword = day_hot_keyword_str.split(':')[0]
        day_hot_keywords.append(day_hot_keyword)
        num += 1
        if num > max_num:
            break

    num = 0
    week_hot_keywords = []
    for week_hot_keyword_str in platforms_json['week_hot_keywords'].split(';'):
        week_hot_keyword = week_hot_keyword_str.split(':')[0]
        week_hot_keywords.append(week_hot_keyword)
        num += 1
        if num > max_num:
            break

    num = 0
    month_hot_keywords = [];
    for month_hot_keyword_str in platforms_json['month_hot_keywords'].split(';'):
        month_hot_keyword = month_hot_keyword_str.split(':')[0];
        month_hot_keywords.append(month_hot_keyword);
        num += 1
        if num > max_num:
            break

    data_info = dict()
    data_info['day_hot_keywords'] = day_hot_keywords
    data_info['week_hot_keywords'] = week_hot_keywords
    data_info['month_hot_keywords'] = month_hot_keywords
    return jsonify(data_info)


# 获取指定个数新闻列表
@app.route('/info/<type>/list/<int:size>', methods=['GET'])
def info_type_list(type,size):

    reader = csv.reader(file('static/data/'+type+'.csv', 'rb'))
    type_list = list()
    max_num = size
    num = 0

    for line in reader:
        if reader.line_num == 1:
            continue
        type_item = dict()
        type_item['item_id'] = line[0].decode('utf-8')
        type_item['author'] = line[4].decode('utf-8')
        type_item['title'] = line[5].decode('utf-8')
        if type == 'ugc':
            type_item['content'] = line[6].decode('utf-8')
        type_item['item_pub_time'] = line[7].decode('utf-8')
        type_list.append(type_item)
        num += 1
        if num >= max_num:
            break

    data_info = {"type_list": type_list}
    return jsonify(data_info)


# 显示新闻详细的信息
@app.route('/info/<type>/<id>', methods=['GET'])
def info_news_detail(type,id):
    reader = csv.reader(file('static/data/'+type+'.csv', 'rb'))
    for line in reader:
        if reader.line_num == 1:
            continue
        if id == line[0]:
            news_item = dict()
            news_item['type'] = type
            news_item['item_id'] = line[0].decode('utf-8')
            news_item['url'] = line[3].decode('utf-8')
            news_item['author'] = line[4].decode('utf-8')
            news_item['title'] = line[5].decode('utf-8')
            news_item['content'] = line[6].decode('utf-8')
            news_item['item_pub_time'] = line[7].decode('utf-8')
            return render_template('info_type_detail.html', data_info=news_item)
    return jsonify({})


# 显示新闻详细的信息，p2p_news_type是新闻类型，p2p_news_source是来源
@app.route('/info/<type>', methods=['GET'])
def info_news(type):
    return render_template("info_type.html", type=type)


@app.route('/info', methods=['GET'])
def news():
    return render_template("info.html")


# 获取平台信息
@app.route('/detail/platforms', methods=['GET'])
def detail_platforms():
    platforms_json = json.load(open('static/data/platforms.json','r'))

    platforms = []
    for platform_json in platforms_json:
        platform_dict = dict()
        platform_dict['platform_name'] = platform_json[u'平台']
        platform_dict['platform_rank'] = platform_json[u'评级']
        platform_dict['platform_index'] = platform_json[u'人气指数']
        platform_dict['platform_earn'] = platform_json[u'平均收益']
        platform_dict['platform_background'] = platform_json[u'平台背景']
        platform_dict['platform_time'] = platform_json[u'上线时间']
        platform_dict['platform_rate'] = platform_json[u'平均利率']
        platform_dict['platform_volume'] = platform_json[u'成交量']
        platform_dict['platform_borrowing_period'] = platform_json[u'平均借款期限']
        platform_dict['platform_need_return'] = platform_json[u'累计待还金额']
        platforms.append(platform_dict)

    data_info = {
        'platforms': platforms
    }
    return jsonify(data_info);


# 显示平台信息
@app.route('/detail/platform/<platform_name>', methods=['GET'])
def detail_info(platform_name):
    # TODO platform_name 返回信息
    platforms_json  = json.load(open('static/data/platforms.json','r'))
    for platform_json in platforms_json:
       if platform_name == platform_json[u'平台']:
           platform_dict = dict()
           platform_dict['platform_name'] = platform_json[u'平台']
           platform_dict['platform_rank'] = platform_json[u'评级']
           platform_dict['platform_index'] = platform_json[u'人气指数']
           platform_dict['platform_earn'] = platform_json[u'平均收益']
           platform_dict['platform_background'] = platform_json[u'平台背景']
           platform_dict['platform_time'] = platform_json[u'上线时间']
           platform_dict['platform_rate'] = platform_json[u'平均利率']
           platform_dict['platform_volume'] = platform_json[u'成交量']
           platform_dict['platform_borrowing_period'] = platform_json[u'平均借款期限']
           platform_dict['platform_need_return'] = platform_json[u'累计待还金额']
           return render_template('detail_info.html', data_info=platform_dict);

    return render_template('detail_info.html', data_info={})


@app.route('/detail')
def detail():
    return render_template("detail.html")


@app.route('/data')
def data():
    return render_template("data.html")


@app.route('/search/<key_word>', methods=['GET'])
def search_info(key_word):
    data_info = {
        'key_word': key_word
    }
    return render_template("search_info.html",data_info=data_info)


@app.route('/search')
def search():
    return render_template("search.html")


@app.route('/invest')
def invest():
    return render_template("invest.html")


@app.route('/datajson', methods=['GET'])
def json_data():
    data0 = {
        'categories': ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子', '羊毛衫', '雪纺衫'],
        'data': [20, 20, 36, 10, 10, 20, 10, 10]
    }
    return jsonify(data0)


@app.route('/datajson2/current=<cur>&rowCount=<ri>&sort[sender]=<sor>&searchPhrase=<sp>')
def json_data2(cur, ri, sor, sp):
    data3 = {
        "cue": cur,
        "ri": ri,
        "sor": sor,
        "sp": sp
    }
    data2 = {
        "current": 1,
        "rowCount": 4,
        "rows": [
            {
                "id": 19,
                "sender": "123@test.de",
                "received": "2014-05-30T22:15:00"
            },
            {
                "id": 14,
                "sender": "123@test.de",
                "received": "2014-05-30T20:15:00"
            },
            {
                "id": 11,
                "sender": "123@test.de",
                "received": "2014-05-30T22:15:00"
            },
            {
                "id": 1,
                "sender": "123@test.de",
                "received": "2014-05-30T20:15:00"
            }
        ],
        "total": 4
    }
    return jsonify(data2)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8086)
