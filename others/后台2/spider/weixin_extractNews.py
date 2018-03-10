#encoding=utf8
'''
    __author__ = 'Administrator'
    2016.3.13 19:50 first version
    从wy163网的html页面里提取结构化新闻数据
'''
import csv
import os
import sys
import bs4
import datetime
import requests, html2text
try:
    from bs4 import BeautifulSoup
except:
    import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')
wy163_dir = r"..\data\news\weixin"



columns = "item_id,item_type,source,url,author,title,content,item_pub_time,tags,cmt_cnt,fav_cnt,gmt_create,exinfo1,exinfo2".split(',')
item_id_dict = {}
writer = csv.writer(file("../data/news/news_other/weixin.csv", 'wb'))
writer.writerow(columns)
def extract_news_txt(soup, news_cnt):
    try:
        is_article = 1
        title = soup[0].strip()
        #print title
        item_pub_time = soup[2].strip()
        #print item_pub_time
        content = soup[3].strip()
        #print metas
        key_words = ""

        url = ""
        description = ""
        image_url = ""


        # print is_article
        # print item_pub_time
        # print title
        # print key_words
        # print description
        # print url
        # print ""
        if is_article == 0:
            return -1
        item_id = "weixin-" + str(news_cnt)
        content = content.replace("\n", "###n###")
        content = content.replace("\r", "###r###")
        content = content.replace("#n#", "###n###")
        content = content.replace("#r#", "###r###")
        gmt_create = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %M:%S")
        cmt_cnt = 0
        fav_cnt = 0
        source = u"微信"


        # print item_id
        item_type = "news"
        tags = key_words.replace(" ", ",")
        #print tags
        # print gmt_create
        # print content
        # print item_pub_time
        exinfo1 = ""
        exinfo2 = ""
        if image_url != "":
            exinfo2 = "image_url:" + image_url

        result = {}
        result['url'] = url
        result['item_id'] = item_id
        result['item_type'] = item_type
        result['author'] = soup[1].strip()
        result['source'] = source
        result['title'] = title
        result['content'] = content
        result['item_pub_time'] = item_pub_time
        result['tags'] = tags
        result['cmt_cnt'] = cmt_cnt
        result['fav_cnt'] = fav_cnt
        result['exinfo1'] = exinfo1
        result['exinfo2'] = exinfo2
        result['gmt_create'] = gmt_create

        line = []
        for col in columns:
            if col not in result:
                line.append('')
            else:
                line.append(str(result[col]).encode('utf-8'))
        writer.writerow(line)
    except Exception, e:
        return -1
    return 0


news_cnt = 0
for cur,dirnames,filenames in os.walk(wy163_dir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for f in os.listdir(cur):
        try:
            f_path = os.path.join(cur, f)
            soup = [line for line in open(f_path)]
            flag = extract_news_txt(soup, news_cnt)
            if flag == 0:
                news_cnt += 1
                print news_cnt
                if news_cnt % 1000 == 1:
                    print news_cnt
        except Exception, e:
            print e
            continue

    #break
print news_cnt
