#encoding=utf8

import os
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import urllib
import urllib2
from HTMLParser import HTMLParser
import csv

myheaders = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': '',
       'Accept-Language': 'zh-CN,zh;en-US,en;q=0.8',
       'Connection': 'keep-alive'}
outpath = "D:/hexunguandian_urls.csv"
content_outpath = "D:/hexunguandian_content.csv"
#outpath = "D:/hexunhangye_urls.csv"
#content_outpath = "D:/hexunhangye_content.csv"

#outpath = "D:/hexunzixun_urls.csv"
#content_outpath = "D:/hexunzixun_content.csv"
#outpath = "D:/hexun_zc_urls.csv"
#content_outpath = "D:/hexun_zc_content.csv"
#data_type = "news"
#data_type = "industry"
data_type = "opinion"
fout = open(outpath, 'wb')
#fcontent_out = open(content_outpath, 'wb')

class HexunZixunParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.urls = []
        self.titles = []
        self.dived = False
        self.aed = False
    
    def handle_starttag(self, tag, attrs):
        if tag == "div":
            for key, value in attrs:
                if key == "id" and value.startswith("infBox"):
                    #print "find one"
                    self.dived = True
        elif tag == "a" and self.dived:
            for key, value in attrs:
                if key == "href":
                    self.urls.append(value)
                    self.dived = False
                    self.aed = True
                    break
        

    
    def handle_data(self, data):
        if self.aed:
            self.titles.append(data)
            self.aed = False
            

class HexunZixunContentParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.content = ""
        self.publish_time = ""
        self.ped = False
        self.contented = False
        self.divNum = 0
        self.title = ""
        self.titled = False
        self.title_h1ed = False
        self.publish_timed = False
        
    def handle_starttag(self, tag, attrs):
        if tag == "div":
            for key, value in attrs:
                if key == "id" and value == "artibody":
                    self.contented = True
                    break
                #if key == "id" and value == "artibodyTitle":
                    #self.titled = True
            self.divNum += 1
        elif tag == "p" and self.contented:
            self.ped = True
        elif tag == "h1":
            self.titled = True
        elif tag == "span":
            for key, value in attrs:
                if key == "id" and value == "pubtime_baidu":
                    self.publish_timed = True
        if self.ped and tag != "p":
            self.ped = False
    
    def handle_data(self, data):
        if self.ped:
            self.content += data
            self.ped = False
        if self.titled:
            self.title = data
            self.titled = False
        if self.publish_timed:
            self.publish_time = data
            self.publish_timed = False
    
    def handle_endtag(self, tag):
        if self.contented and tag == "div":
            if self.divNum == 0:
                self.contented = False
            else:
                self.divNum -= 1
        #if self.ped and tag == "p":
            #self.ped = False
        

def CrawlUrl(url):
    req = urllib2.Request(url, headers=myheaders)
    iter = 3
    while iter > 0:
        try:
            #html = urllib2.urlopen(req).read()
            rsp = urllib2.urlopen(req)
            html = rsp.read()
            #print html
            encoding = rsp.info().getparam("charset")
            html = html.decode("gb18030").encode("utf-8")
            #print html
            #print "encoding :" + encoding
            #print type(encoding)
            #if encoding != "utf8" or encoding != "utf-8":
                #html = html.decode(encoding).encode("utf-8")
            return html
        except Exception, e:
            print e
            print "urllib error : " + " iter : " + str(iter) + "\n"
            iter -= 1
            if iter == 0:
                print url + " cannot crawl...\n"
                return None   

def GetHexunLatest(url):

    #myheaders = { 'User-Agent' : user_agent }
    html = CrawlUrl(url)
    try:
        #parser = WangDaiInfoParser()   
        parser = HexunZixunParser()
        parser.feed(html)
        parser.close()
        count = len(parser.urls)
        if len(parser.urls) != len(parser.titles):
            print "len not equal : " + len(parser.urls) + " " + len(parser.titles)
        for i in range(count):
            #print url
            fout.write(parser.urls[i] + ',' + parser.titles[i] + '\n')
        fout.close()
    except Exception, e:
        print "parser error : ", e
        return
    #urls.extend(parser.urls)
    #print len(parser.urls)
    #fout.write(parser.platform_name +"," + parser.problem +","+ parser.happen_time +","+ "\n")
        #print parser.rootUrl+url
    print "finish " + url 



def GetHexunZixunContent():
    fin = open(outpath, "rb")
    assert(fin)
    writer = csv.writer(file(content_outpath, "wb"))
    writer.writerow(["url", "data_type", "title", "publish_time", "content"])
    num = 0
    for line in fin.readlines():
        url = line.split(',')[0]
        html = CrawlUrl(url)
        parser = HexunZixunContentParser()
        try:
            parser.feed(html)
            parser.close()
        except Exception, e:
            print e.message + "\n"
            #fcontent_out.write(url + ',' + "\n")
            writer.writerow([url, data_type, "", "", ""])
            continue
        #content = parser.content.replace("\r\n", "###NEWLINE###")
        #content = content.replace(",", "###COMMA###")
        #fcontent_out.write(url + ',' + parser.title + ',' + content + '\n')
        writer.writerow([url, data_type, parser.title, parser.publish_time, parser.content])
        num += 1
        if num % 10 == 0:
            print "num :" + str(num) + "\n"
        #break
    #fcontent_out.close()
        

if __name__ == "__main__":
    url = "http://p2p.hexun.com/gd/"
    #url = "http://p2p.hexun.com/hy/"
    #url = "http://p2p.hexun.com/zx/"
    #url = "http://p2p.hexun.com/zc/"
    GetHexunLatest(url)
    GetHexunZixunContent()
            
                    
                    
    
        

#from splinter.browser import Browser
#from time import sleep

#b = Browser(driver_name="chrome")
#b.visit("http://p2p.hexun.com/zx/")
#while True:
    #try:
        #button = b.find_by_id("listMore")
        #button.click()
    #except Exception, e:
        #break

#try:
    #ans_list = b.find_by_id("")

#b.quit()