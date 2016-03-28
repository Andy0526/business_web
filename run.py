# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
import json
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
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
        type_item['item_id'] = reader.line_num
        type_item['author'] = line[4].decode('utf-8')
        type_item['title'] = line[5].decode('utf-8')
        if type == 'ugc' or type == 'opinion':
            type_item['content'] = line[6].decode('utf-8')
        type_item['item_pub_time'] = line[7].decode('utf-8')
        type_list.append(type_item)
        num += 1
        if num >= max_num:
            break

    data_info = {"type_list": type_list}
    return jsonify(data_info)


# 分页获取 current=0&rowCount=15
@app.route('/info/<type>/list/current=<int:cur>&rowCount=<int:rows>', methods=['GET'])
def info_type_list_sub(type, cur, rows):
    reader = csv.reader(file('static/data/'+type+'.csv', 'rb'))
    type_list = list()
    start_num = cur * rows
    end_num = (cur + 1) * rows
    num = 0
    for line in reader:
        if reader.line_num == 1:
            continue
        if (num >= start_num) and (num < end_num):
            type_item = dict()
            type_item['item_id'] = reader.line_num
            type_item['author'] = line[4].decode('utf-8')
            type_item['title'] = line[5].decode('utf-8')
            if type == 'ugc' or type == 'opinion':
                type_item['content'] = line[6].decode('utf-8')
            type_item['item_pub_time'] = line[7].decode('utf-8')
            type_list.append(type_item)
        num += 1
        if num > end_num:
            break

    data_info = {
        "type_list": type_list
    }
    return jsonify(data_info)


# 获取指定个数新闻列表
@app.route('/info/<type>/list/size', methods=['GET'])
def info_type_list_size(type):
    reader = csv.reader(file('static/data/'+type+'.csv', 'rb'))
    list_size = 0
    for line in reader:
        if reader.line_num == 1:
            continue
        list_size += 1
    data_info = {"list_size": list_size}
    return jsonify(data_info)


# 显示新闻详细的信息
@app.route('/info/<type>/<int:id>', methods=['GET'])
def info_news_detail(type,id):
    reader = csv.reader(file('static/data/'+type+'.csv', 'rb'))
    for line in reader:
        if reader.line_num == 1:
            continue
        if id == reader.line_num:
            news_item = dict()
            news_item['type'] = type
            news_item['item_id'] = line[0].decode('utf-8')
            news_item['url'] = line[3].decode('utf-8')
            news_item['author'] = line[4].decode('utf-8')
            news_item['title'] = line[5].decode('utf-8')
            if type == 'opinion' :
                 content = line[6].decode('utf-8')
                 content = content.replace("#n#", "")
                 content = content.replace("#r#", "")
                 content = content.replace(" ", "")
                 content = content[0:20]+"..."
                 news_item['title'] = content
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
    return jsonify(data_info)


# 获取某一平台信息
@app.route('/detail/platform/<platform_name>/info', methods=['GET'])
def detail_platform(platform_name):
    # TODO platform_name 返回信息
    platforms_json = json.load(open('static/data/platforms.json', 'r'))
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

            # 评论标签
            all_comment_json = json.load(open('static/data/plat_top_labels_sentiment.json', 'r'))
            comment_json = all_comment_json.get(platform_name, {u'frequent_label': [], u'sentiment': 0})
            comment_map_list = comment_json.get(u'frequent_label')
            # 转换成 name value 形式
            comment_list = list()
            for comment_map in comment_map_list:
                for (k, v) in comment_map.items():
                    comment_list.append({'name': k, 'value': v})
            platform_dict['frequent_label'] = comment_list
            return jsonify(platform_dict)

    return jsonify({})


# 获取某一平台最新信息
@app.route('/detail/platform/<platform_name>/news/recent', methods=['GET'])
def detail_platform_news_recent(platform_name):
        recent_news_json = json.load(open('static/data/plat_recent_news.json', 'r'))
        recent_news_list = recent_news_json.get(platform_name, [])
        platform_dict = dict()
        platform_dict['recent_news_list'] = recent_news_list
        return jsonify(platform_dict)


# 获取某一平台相关信息
@app.route('/detail/platform/<platform_name>/news/related', methods=['GET'])
def detail_platform_news_related(platform_name):
        related_news_json = json.load(open('static/data/plat_related_news.json', 'r'))
        related_news_list = related_news_json.get(platform_name, [])
        platform_dict = dict()
        platform_dict['related_news_list'] = related_news_list
        return jsonify(platform_dict)


# 显示平台信息
@app.route('/detail/platform/<platform_name>', methods=['GET'])
def detail_info(platform_name):
    return render_template('detail_info.html', platform_name=platform_name)


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
    return render_template("search_info.html", data_info=data_info)


@app.route('/search')
def search():
    return render_template("search.html")


@app.route('/invest')
def invest():
    return render_template("invest.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8086)
