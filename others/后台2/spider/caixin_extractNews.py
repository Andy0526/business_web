#encoding=utf8
'''
    __author__ = 'Administrator'
    2016.3.13 19:50 first version
    从caixin网的html页面里提取结构化新闻数据
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
caixin_dir = r"C:\Users\Administrator\Desktop\Working Folder\Holmes\data\news\caixin"



columns = "item_id,item_type,source,url,author,title,content,item_pub_time,tags,cmt_cnt,fav_cnt,gmt_create,exinfo1,exinfo2".split(',')
item_id_dict = {}
writer = csv.writer(file("../data/news/news_other/caixin.csv", 'wb'))
writer.writerow(columns)
def extract_news(soup):
    try:
        metas = soup.find_all("meta")
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
            if meta.has_attr("property") == True:
                if meta["content"] == "article":
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
        def has_class__id(tag):
            return tag.has_attr('class') and tag.has_attr('id')
        news_id = url.split("/")[4]
        item_id = "caixin-" + news_id[:news_id.find(".")]
        if item_id not in item_id_dict:
            item_id_dict.setdefault(item_id, 0)
        else:
            return
        content = ""
        item_pub_time = ""
        for the_content in soup.find_all(id="the_content"):
            time_info = the_content.find(id="artInfo").contents[0]
            item_pub_time = time_info[time_info.find("2"):time_info.find("日")+len(u"日")]
            item_pub_time = item_pub_time.replace("年", "-").replace("月", "-").replace("日", "")

            ppp = the_content.find(class_="media ")
            if ppp != None:
                image_url =  ppp.find("img")["src"]
                # print image_url
            #print the_content
            content_list = the_content.find(id="Main_Content_Val").contents
            #■结束符
            for p in content_list[1:]: #第一行是回车
                if type(p) == bs4.element.NavigableString:
                    content += p
                elif type(p) == bs4.element.Tag:
                    if p.name == "p":
                        for ele in p.contents:
                            if type(ele) == bs4.element.NavigableString:
                                content += ele
                            elif ele.name == "strong":
                                for ele2 in ele.contents:
                                    if type(ele2) == bs4.element.NavigableString:
                                        content += ele2

        if content.find("■") != -1:
            content = content[:content.find("■")]
        content = content.replace("\n", "###n###")
        content = content.replace("\r", "###r###")
        gmt_create = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %M:%S")
        cmt_cnt = 0
        fav_cnt = 0
        source = u"财新网"


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
        result['author'] = 'caixin_jizhe'
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
for cur,dirnames,filenames in os.walk(caixin_dir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for dir in  dirnames:
        dir_path = os.path.join(cur, dir)
        cnt = 0
        for f in os.listdir(dir_path):
            try:
                f_path = os.path.join(dir_path, f)
                soup = BeautifulSoup(open(f_path))
                if soup == None or soup.find("title") == None:
                    continue
                title =  soup.find("title").string
                ##初步过滤
                if len(title.split("_")) < 3 \
                    or title.split("_")[2] == "CAIXIN.COM"\
                        or title.split("_")[2] != "财新网":
                    continue
                # print f_path
                # print title
                flag = extract_news(soup)
                if flag == 0:
                    news_cnt += 1
                    print title
                if news_cnt % 1000 == 1:
                    print news_cnt
            except Exception, e:
                print e
                continue

        #break
print news_cnt
print len(item_id_dict)