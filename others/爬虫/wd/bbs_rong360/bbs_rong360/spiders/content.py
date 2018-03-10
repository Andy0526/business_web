# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os
import json
import scrapy

class ContentSpider(scrapy.Spider):
	name = "content"
	start_urls = []

	def __init__(self):
		df = open("融360.csv", "w")
		df.write("item_id,item_type,source,url,author,title,content,item_pub_time,tags,cmt_cnt,fav_cnt,gmt_create,exinfo1,exinfo2\n")
		df.close()
		for f in os.listdir("html"):
			self.start_urls.append("file:///Users/ziaoang/Documents/p2p/bbs_rong360/html/" + f)

	def parse(self, response):
		id = response.url.split("/")[-1].replace(".html","")
		title = response.xpath('//span[@id="thread_subject"]/text()').extract()[0]

		df = open("融360.csv", "a")
		tids = response.xpath('//div[re:test(@id, "post_\d+$")]/@id').extract()
		for i in range(len(tids)):
			try:
				tid = tids[i].replace("post_","")
				time = response.xpath('//em[@id="authorposton%s"]/text()'%tid).extract()[0].replace("发表于 ","")
				content = "".join(response.xpath('//td[@id="postmessage_%s"]//text()'%tid).extract())
				content = '"' + content.strip().replace("\r","#r#").replace("\n","#n#").replace("\t","#t#") + '"'
				url = "http://bbs.rong360.com/thread-%s-1.html"%id
				if i == 0:
					df.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(id,"opinion","融360",url,"",title,content,time,"","","","","",""))
				else:
					df.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(id,"reply","融360",url,"","",content,time,"","","","","",""))
			except:
				pass
		df.close()
		








