#encoding=utf8
'''
    __author__ = 'Administrator'
    2016.3.13 19:50 first version
    从sina网的html页面里提取结构化新闻数据
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
sina_dir = r"F:\LoalaSave\finance.sina.com.cn"



columns = "item_id,item_type,source,url,author,title,content,item_pub_time,tags,cmt_cnt,fav_cnt,gmt_create,exinfo1,exinfo2".split(',')
item_id_dict = {}
writer = csv.writer(file("../data/news/news_other/sina.csv", 'wb'))
writer.writerow(columns)
def extract_news(soup, news_cnt):
    try:
        metas = soup.find_all("meta")
        #print metas
        key_words = ""
        is_article = 0
        title = ""
        url = ""
        description = ""
        image_url = ""

        for meta in metas:
            if meta.has_attr("name") == True:
                if meta["name"] == "keywords":
                    key_words = meta["content"]
                if meta["name"] == "weibo: article:create_at":
                    # print meta["content"]
                    item_pub_time = meta["content"].split(" ")[0]
                    # print item_pub_time
            if meta.has_attr("property") == True:
                if meta["content"] == "news":
                    is_article = 1
                if meta["property"] == "og:title":
                    title = meta["content"]
                if meta["property"] == "og:url":
                    url = meta["content"]
                if meta["property"] == "og:description":
                    description = meta["content"]

        # print title
        # print key_words
        # print description
        # print url
        # print ""
        if is_article == 0:
            return -1
        item_id = "sina-" + str(news_cnt)
        content = ""
        #share BSHARE_POP blkContainerSblkCon clearfix blkContainerSblkCon_14
        content_div = soup.find(name="div", id="artibody")
        #print content_div
        p_list = content_div.find_all("p")
        #print p_list
        for i in xrange(len(p_list)):
            p = ""
            for e in  p_list[i].contents:
                try:
                    p += e.string
                except Exception:
                    continue
            content += p + "\n"
        content = content.replace("\n", "###n###")
        content = content.replace("\r", "###r###")
        gmt_create = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %M:%S")
        cmt_cnt = 0
        fav_cnt = 0
        source = u"新浪财经"


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
        result['author'] = 'sina_jizhe'
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
for cur,dirnames,filenames in os.walk(sina_dir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for f in os.listdir(cur):
        print "#", f
        try:
            f_path = os.path.join(cur, f)
            soup = BeautifulSoup(open(f_path))
            if soup == None or soup.find("title") == None:
                continue
            title =  soup.find("title").string
            ##初步过滤
            if len(title.split("_")) < 3 \
                    or title.split("_")[2] != "新浪网":
                continue
            # print f_path
            # print title
            flag = extract_news(soup, news_cnt)
            if flag == 0:
                news_cnt += 1
                print news_cnt
                #print title
            if news_cnt % 1000 == 1:
                print news_cnt
        except Exception, e:
            print e
            continue

    #break
print news_cnt
print len(item_id_dict)