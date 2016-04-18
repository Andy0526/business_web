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


@app.route('/yqdp')
def yqdp():
    return render_template("yqdp.html")


@app.route('/info/hot/topic/<int:topic_id>')
def info_hot_topic(topic_id):
    return render_template("info_hot_topic.html",topic_id = topic_id)


@app.route('/info/hot/topic/preview/<topic_id>')
def info_hot_topic_preview(topic_id):
    news_json = json.load(open('static/data/hot_topic/'+topic_id+'/news.json', 'r'))
    item_list = []
    for json_item in news_json['item_list']:
        item = dict()
        item['_id'] = json_item['_id']
        item['title'] = json_item['title']
        item['item_pub_time'] = json_item['item_pub_time']
        item_list.append(item)

    keywords_json = json.load(open('static/data/hot_topic/'+topic_id+'/keywords.json', 'r'))
    max_num = 60
    num = 0
    keyword_list = []
    for name in keywords_json:
        keyword_map = dict()
        keyword_map['name'] = name
        keyword_map['value'] = keywords_json[name]
        keyword_list.append(keyword_map)
        num += 1
        if num > max_num:
            break

    # 热度变化
    hot_dict_json = json.load(open('static/data/hot_topic/'+topic_id+'/hot.json', 'r'))
    hot_dict = dict()
    hot_x = sorted(hot_dict_json)
    hot_y = list()
    for key in hot_x:
        hot_y.append(hot_dict_json[key])
    hot_dict = {
        'x': hot_x,
        'y': hot_y
    }

    data_info = {
        "item_list": item_list,
        "keyword_list": keyword_list,
        "hot_map": hot_dict
    }
    return jsonify(data_info)


@app.route('/info/hot/topic/news/detail/<topic_id>/<news_id>')
def info_hot_topic_news_detail(topic_id,news_id):
    news_json = json.load(open('static/data/hot_topic/'+topic_id+'/news.json', 'r'))
    for json_item in news_json['item_list']:
        if json_item['_id'] == news_id:
            return render_template('info_hot_topic_news_detail.html', data_info=json_item)
    return render_template('info_hot_topic_news_detail.html', data_info={})


# 新闻 >> 热点
@app.route('/info/hot', methods=['GET'])
def info_hot():
    platforms_json = json.load(open('static/data/hot_keyword.json', 'r'))
    max_num = 60

    num = 0
    day_hot_keywords = []
    for day_hot_keyword_str in platforms_json['day_hot_keywords'].split(';'):
        day_map = dict()
        day_map['name'] = day_hot_keyword_str.split(':')[0]
        day_map['value'] = day_hot_keyword_str.split(':')[1]
        day_hot_keywords.append(day_map)
        num += 1
        if num > max_num:
            break
    num = 0
    week_hot_keywords = []
    for week_hot_keyword_str in platforms_json['week_hot_keywords'].split(';'):
        week_map = dict()
        week_map['name'] = week_hot_keyword_str.split(':')[0]
        week_map['value'] = week_hot_keyword_str.split(':')[1]
        week_hot_keywords.append(week_map)
        num += 1
        if num > max_num:
            break

    num = 0
    month_hot_keywords = []
    for month_hot_keyword_str in platforms_json['month_hot_keywords'].split(';'):
        month_map = dict()
        month_map['name'] = month_hot_keyword_str.split(':')[0]
        month_map['value'] = month_hot_keyword_str.split(':')[1]
        month_hot_keywords.append(month_map)
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
def info_type_list(type, size):
    type_list = list()
    max_num = size
    num = 0
    if type == 'ugc':
        reader = csv.reader(file('static/data/'+type+'.csv', 'rb'))
        for line in reader:
            if reader.line_num == 1:
                continue
            type_item = dict()
            type_item['_id'] = line[0].decode('utf-8')
            type_item['author'] = line[4].decode('utf-8')
            type_item['title'] = line[5].decode('utf-8')
            type_item['content'] = line[6].decode('utf-8')
            type_item['item_pub_time'] = line[7].decode('utf-8')
            type_list.append(type_item)
            num += 1
            if num >= max_num:
                break
    else:
        reader = json.load(open('static/data/'+type+'.json', 'r'))
        for line in reader:
            type_list.append(line)
            num += 1
            if num >= max_num:
                break
    data_info = {"type_list": type_list}
    return jsonify(data_info)


# 分页获取 current=0&rowCount=15
@app.route('/info/<type>/list/current=<int:cur>&rowCount=<int:rows>', methods=['GET'])
def info_type_list_sub(type, cur, rows):

    type_list = list()
    start_num = cur * rows
    end_num = (cur + 1) * rows
    num = 0

    if type == 'ugc':
        reader = csv.reader(file('static/data/'+type+'.csv', 'rb'))
        for line in reader:
            if reader.line_num == 1:
                continue
            if (num >= start_num) and (num < end_num):
                type_item = dict()
                type_item['_id'] = line[0].decode('utf-8')
                type_item['author'] = line[4].decode('utf-8')
                type_item['title'] = line[5].decode('utf-8')
                if type == 'ugc' or type == 'opinion':
                    type_item['content'] = line[6].decode('utf-8')
                type_item['item_pub_time'] = line[7].decode('utf-8')
                type_list.append(type_item)
            num += 1
            if num >= end_num:
                break
    else:
        reader = json.load(open('static/data/'+type+'.json', 'r'))
        for line in reader:
            if (num >= start_num) and (num < end_num):
                type_list.append(line)
            num += 1
            if num >= end_num:
                break

    data_info = {"type_list": type_list}
    return jsonify(data_info)


# 获取指定个数新闻列表
@app.route('/info/<type>/list/size', methods=['GET'])
def info_type_list_size(type):
    if type != 'ugc':
        reader = json.load(open('static/data/'+type+'.json', 'r'))
        data_info = {"list_size": len(reader)}
        return jsonify(data_info)

    reader = csv.reader(file('static/data/'+type+'.csv', 'rb'))
    list_size = 0
    for line in reader:
        if reader.line_num == 1:
            continue
        list_size += 1
    data_info = {"list_size": list_size}
    return jsonify(data_info)


# 显示新闻详细的信息
@app.route('/info/<type>/<id>', methods=['GET'])
def info_news_detail(type,id):
    if type != 'ugc':
        reader = json.load(open('static/data/'+type+'.json', 'r'))
        for line in reader:
            if id == line['_id']:
                line['type'] = type
                return render_template('info_type_detail.html', data_info=line)

    reader = csv.reader(file('static/data/'+type+'.csv', 'rb'))
    for line in reader:
        if reader.line_num == 1:
            continue
        if id == line[0].decode('utf-8'):
            news_item = dict()
            news_item['type'] = type
            news_item['_id'] = line[0].decode('utf-8')
            news_item['url'] = line[3].decode('utf-8')
            news_item['author'] = line[4].decode('utf-8')
            news_item['title'] = line[5].decode('utf-8')
            if type == 'opinion':
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
    platforms_json = json.load(open('static/data/platform_info.json','r'))
    platforms = []
    for platform_name in platforms_json:
        platform_dict = platforms_json[platform_name]
        platform_dict['platform_name'] = platform_name
        platforms.append(platform_dict)

    recent_reviews_list = json.load(open('static/data/recent_reviews.json', 'r'))
    data_info = {
        'platforms': platforms,
        'recent_reviews_list': recent_reviews_list
    }
    return jsonify(data_info)


# 获取问题平台信息
@app.route('/detail/problem_platforms', methods=['GET'])
def detail_problem_platforms():
    platforms_json = json.load(open('static/data/problem_platform.json','r'))

    platforms = []
    num = 0
    for platform_json in platforms_json:
        platform_dict = dict()
        platform_dict['platform_name'] = platform_json['platform_name']
        platform_dict['event_type'] = platform_json['event_type']
        platform_dict['problem_time'] = platform_json['problem_time']
        platform_dict['region'] = platform_json['region']
        platform_dict['online_time'] = platform_json['online_time']
        platform_dict['registration_capital'] = platform_json['registration capital']
        platforms.append(platform_dict)
        num += 1
        if num >= 1000:
            break

    data_info = {
        'platforms': platforms
    }
    return jsonify(data_info)


# 获取某一平台信息
@app.route('/detail/platform/<platform_name>/info', methods=['GET'])
def detail_platform(platform_name):
    platform_dict = get_platform_detail_info(platform_name)
    return jsonify(platform_dict)


def get_platform_detail_info(platform_name):
    platforms_json = json.load(open('static/data/platform_info.json','r'))
    if not (platform_name in platforms_json):
        return {}

    platform_dict = platforms_json[platform_name]
    platform_dict['platform_name'] = platform_name

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

    # 相关图表
    all_chart_json = json.load(open('static/data/charts_data.json', 'r'))
    chart_json = all_chart_json.get(platform_name, {})
    platform_dict['chart_json'] = chart_json

    # 评论列表
    comments_data_map = json.load(open('static/data/comments_data.json','r'))
    comments_data_list = comments_data_map.get(platform_name, [])
    platform_dict['comments_data_list'] = comments_data_list

    # 新闻
    recent_news_json = json.load(open('static/data/plat_recent_news.json', 'r'))
    recent_news_list = recent_news_json.get(platform_name, [])
    platform_dict['recent_news_list'] = recent_news_list

    related_news_json = json.load(open('static/data/plat_related_news.json', 'r'))
    related_news_list = related_news_json.get(platform_name, [])
    platform_dict['related_news_list'] = related_news_list

    # 新闻关键词
    platform_news_keywords = json.load(open('static/data/platform_news_keywords.json', 'r'))
    max_num = 60
    num = 0
    keyword = []
    keywords_list = platform_news_keywords.get(platform_name, [])
    for item_list in keywords_list:
        keyword_map = dict()
        keyword_map['name'] = item_list[0]
        keyword_map['value'] = item_list[1]
        keyword.append(keyword_map)
        num += 1
        if num > max_num:
            break
    platform_dict['keyword'] = keyword

    # 评论
    platform_reviews_v2 = json.load(open('static/data/platform_reviews_v4.json', 'r'))
    reviews_map = platform_reviews_v2.get(platform_name, {"reviews": {}})
    reviews = reviews_map.get("reviews")
    platform_dict['reviews'] = reviews

    return platform_dict


# 显示平台信息
@app.route('/detail/platform/<platform_name>', methods=['GET'])
def detail_info(platform_name):
    return render_template('detail_info.html', platform_name=platform_name)


@app.route('/detail/rank')
def detail_rank():
    return render_template("detail_rank.html")


@app.route('/detail/navigation')
def detail_navigation():
    return render_template("detail_navigation.html")


@app.route('/detail/problem')
def detail_problem():
    return render_template("detail_problem.html")


@app.route('/detail/problem_analyze')
def detail_problem_analyze():
    return render_template("detail_problem_analyze.html")


@app.route('/search/<platform_name>', methods=['GET'])
def search_info(platform_name):
    platforms_json = json.load(open('static/data/platform_info.json','r'))
    if not (platform_name in platforms_json):
        return render_template("search_not_found.html")
    return render_template("search_detail_info.html", platform_name=platform_name)


@app.route('/ptpx', methods=['GET'])
def ptpx():
    return render_template("ptpx.html")


@app.route('/ptpx/platform_name_list', methods=['GET'])
def ptpx_platform_name_list():
    platforms_json = json.load(open('static/data/platform_info.json','r'))
    platform_name_list = list()
    for platform_name in platforms_json:
        platform_name_list.append(platform_name)
    platform_dict = {"platform_name_list":platform_name_list}
    return jsonify(platform_dict)


@app.route('/search')
def search():
    return render_template("search.html")


@app.route('/invest')
def invest():
    return render_template("invest.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6086, threaded=True)
