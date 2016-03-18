# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# 主页
@app.route('/')
def default():
    return render_template("home.html")


# 主页
@app.route('/home')
def home():
    return render_template("home.html")


# 显示新闻详细的信息，p2p_news_type是新闻类型，p2p_news_source是来源，p2p_news_id是新闻的唯一标识
# 例如：/news/行业相关/p2p观察网/12
@app.route('/news/<p2p_news_type>/<p2p_news_source>/<p2p_news_id>', methods=['GET'])
def news_detail(p2p_news_type, p2p_news_source, p2p_news_id):
    # TODO 根据 p2p_news_source p2p_news_id 查找到 p2p_news_info
    p2p_news_info = {
        'title': u"P2P到了最危险的时候了吗？",
        'author': u"P2P观察网",
        'date': u"2015/9/20 11:23:28",
        'url': u"http://www.p2pguancha.com/news/77.html",
        'content': u"#n#        #n#        专栏作者：朱飞，微信公众号zhufei101运营者最近一段时间，“两文件”和“一行动”让P2P行业笼上一层阴霾。两文件指的是《关于促进互联网金融健康发展的指导意见》和《非银行支付机构网络支付业务管理办法》；一行动则是“经侦来敲门”。朱飞注意到，这些“利空”出现后，一些从业者选择表达“异见”，希望“上达天听”，从而对还未出台的正式监管细则产生正面影响；另一部分人则“痛定思痛”，“戴着脚镣练习跳舞”，积极调整姿势去迎合“圣意”。不得不说，这两类做法都值得肯定。前一类人，他们不仅是在为自己争取利益，也在为行业谋福利。而后一种方式，看上去有些没出息，但何尝不是在中国做生意的最正确的姿势！扯淡打住，回到正题，P2P真的到了最危险的时候了吗？先看几条消息：1、P2P今年前8月融资次数超过过去5年总和21世纪经济报道的数据显示，2015年前8个月，P2P平台已完成58次融资，超过过去五年总和。这些获得风投的P2P平台主要集中在北上广等一线城市。其中，北京25家、上海24家和广东13家，约占总数的75%。这说明什么？这表明在人人都谈资本寒冬的时刻，互联网金融并没有被波及。以红杉中国的投资项目为例，2015年迄今的前8个月中，红杉中国共投资的金融项目就高达7个。VC资本方向来被视为是一群卓有远见的聪明人，他们押注互联网金融，显然对未来充满希望。2、互联网金融产品网民渗透率达到68.1%在9月16日举行的“2015中国国际互联网+金融博览会”新闻发布会上，中国电子商务协会副秘书长李建华透露，截至2015年上半年，我国互联网金融产品网民渗透率为68.1%。当然，这里的互联网金融不限于P2P，而是包括第三方支付、P2P网络借贷、股权众筹融资、互联网基金销售、互联网保险、互联网信托和互联网消费金融等在内。这又说明什么？简单了说就是互联网金融大势所趋不可逆转，往深了说这是“民智已开”，传统银行躺着赚钱的事实已被各类互联网金融产品解剖扒皮，200万亿的金融市场需要被重新洗牌和分配。3、P2P收益率两年缩水一半据网贷之家的数据显示，在2013年7月，整个网贷行业的综合收益率达到了26.35%的最高点，而到了2015年8月，这一数据为12.98%，收益率水平在25个月里跌了超过一半。这咋一看是个负面消息，其实百益无一害。P2P一直被诟病收益太高不靠谱，如今利率逐渐下调–但仍高于银行定存和理财–正是挣回信任的好时机。哪怕P2P平均收益降至6%-10%，加上强体验、低门槛，也足以抵消银行“安全”这一唯一优势。不再多举利好消息了，资本环境、市场环境都表明，P2P仍然是广阔天地大有作为。尽管“事故”仍时有发生，但不影响远大抱负的平台升级加码–正如巴菲特所言，“市场行情最不好的时候，正是投资未来的节点。”何况当前市场行情并未缩水，“利空”的仅仅是政策动作而已。而至于政策，朱飞想引用一位银行家朋友的话（被要求不具名）来为本位收尾，他给出了另一些角度的解读：1、政策关上一扇门，必然打开一扇窗。近期按规定不能经营托管业务的第三方机构开始寻求与银行联合托管，或者转型更大的消费金融市场，未尝不是一条出路。2、监管不是万能钥匙，靠监管套利求生存的公司，本身就不具备强劲的生命力。迎难而上才能炼成一家经得起摸爬滚打的公司。3、还仅仅是《指导意见》和“征求意见稿”。        #n#               #n#"
    }

    data_info = {
        'p2p_news_type': p2p_news_type,
        'p2p_news_source': p2p_news_source,
        'p2p_news_info': p2p_news_info
    }

    return render_template("news_info.html", data_info=data_info)


# 显示新闻详细的信息，p2p_news_type是新闻类型，p2p_news_source是来源
# 例如：/news/行业相关/p2p观察网
@app.route('/news/<p2p_news_type>/<p2p_news_source>', methods=['GET'])
def news_source(p2p_news_type, p2p_news_source):
    # TODO 根据 p2p_news_source 查找到  p2p_news_info_list

    title = u"P2P到了最危险的时候了吗？"
    if len(title) > 20:
        title = title[0:20]+"..."

    content = u"#n#        #n#        专栏作者：朱飞，微信公众号zhufei101运营者最近一段时间，“两文件”和“一行动”让P2P行业笼上一层阴霾。两文件指的是《关于促进互联网金融健康发展的指导意见》和《非银行支付机构网络支付业务管理办法》；一行动则是“经侦来敲门”。朱飞注意到，这些“利空”出现后，一些从业者选择表达“异见”，希望“上达天听”，从而对还未出台的正式监管细则产生正面影响；另一部分人则“痛定思痛”，“戴着脚镣练习跳舞”，积极调整姿势去迎合“圣意”。不得不说，这两类做法都值得肯定。前一类人，他们不仅是在为自己争取利益，也在为行业谋福利。而后一种方式，看上去有些没出息，但何尝不是在中国做生意的最正确的姿势！扯淡打住，回到正题，P2P真的到了最危险的时候了吗？先看几条消息：1、P2P今年前8月融资次数超过过去5年总和21世纪经济报道的数据显示，2015年前8个月，P2P平台已完成58次融资，超过过去五年总和。这些获得风投的P2P平台主要集中在北上广等一线城市。其中，北京25家、上海24家和广东13家，约占总数的75%。这说明什么？这表明在人人都谈资本寒冬的时刻，互联网金融并没有被波及。以红杉中国的投资项目为例，2015年迄今的前8个月中，红杉中国共投资的金融项目就高达7个。VC资本方向来被视为是一群卓有远见的聪明人，他们押注互联网金融，显然对未来充满希望。2、互联网金融产品网民渗透率达到68.1%在9月16日举行的“2015中国国际互联网+金融博览会”新闻发布会上，中国电子商务协会副秘书长李建华透露，截至2015年上半年，我国互联网金融产品网民渗透率为68.1%。当然，这里的互联网金融不限于P2P，而是包括第三方支付、P2P网络借贷、股权众筹融资、互联网基金销售、互联网保险、互联网信托和互联网消费金融等在内。这又说明什么？简单了说就是互联网金融大势所趋不可逆转，往深了说这是“民智已开”，传统银行躺着赚钱的事实已被各类互联网金融产品解剖扒皮，200万亿的金融市场需要被重新洗牌和分配。3、P2P收益率两年缩水一半据网贷之家的数据显示，在2013年7月，整个网贷行业的综合收益率达到了26.35%的最高点，而到了2015年8月，这一数据为12.98%，收益率水平在25个月里跌了超过一半。这咋一看是个负面消息，其实百益无一害。P2P一直被诟病收益太高不靠谱，如今利率逐渐下调–但仍高于银行定存和理财–正是挣回信任的好时机。哪怕P2P平均收益降至6%-10%，加上强体验、低门槛，也足以抵消银行“安全”这一唯一优势。不再多举利好消息了，资本环境、市场环境都表明，P2P仍然是广阔天地大有作为。尽管“事故”仍时有发生，但不影响远大抱负的平台升级加码–正如巴菲特所言，“市场行情最不好的时候，正是投资未来的节点。”何况当前市场行情并未缩水，“利空”的仅仅是政策动作而已。而至于政策，朱飞想引用一位银行家朋友的话（被要求不具名）来为本位收尾，他给出了另一些角度的解读：1、政策关上一扇门，必然打开一扇窗。近期按规定不能经营托管业务的第三方机构开始寻求与银行联合托管，或者转型更大的消费金融市场，未尝不是一条出路。2、监管不是万能钥匙，靠监管套利求生存的公司，本身就不具备强劲的生命力。迎难而上才能炼成一家经得起摸爬滚打的公司。3、还仅仅是《指导意见》和“征求意见稿”。        #n#               #n#";
    content = content.replace('#n#', '')
    content = content.replace(' ', '')
    content = u">> "+content[0:72]+"..."

    p2p_news_info_0 = {
        'id': 10,
        'title': title,
        'abstract': content
    }

    p2p_news_info_list = {
        'id0': p2p_news_info_0,
        'id1': p2p_news_info_0,
        'id2': p2p_news_info_0,
        'id3': p2p_news_info_0,
        'id4': p2p_news_info_0,
        'id5': p2p_news_info_0,
        'id6': p2p_news_info_0
    }

    data_info = {
        'p2p_news_type': p2p_news_type,
        'p2p_news_source': p2p_news_source,
        'p2p_news_info_list': p2p_news_info_list
    }

    return render_template("news_source.html", data_info=data_info)


# 显示平台信息
@app.route('/detail/<platform_id>', methods=['GET'])
def detail_info(platform_id):
    # TODO 根据platform_id 返回信息
    data_info = {
        'platform_id': platform_id,
        'platform_name': u'陆金所',
        'platform_type': u'信用贷',
        'platform_status': u'running',
        'company': u'所属公司',
        'need_invest': u'123',
        'prospect_earn': u'21%~45%',
        'Risk_weight': 2,
        'source': u'来源',
        'source_url': u'来源链接',
    }
    return render_template('detail_info.html', data_info=data_info)


@app.route('/news', methods=['GET'])
def news():
    return render_template("news.html")


@app.route('/detail')
def detail():
    return render_template("detail.html")


@app.route('/data')
def data():
    return render_template("data.html")


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
