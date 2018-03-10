# -*- coding: utf-8 -*-

import scrapy

class BbsSpider(scrapy.Spider):
	name = "bbs"
	start_urls = []

	def __init__(self):
		for page in range(1, 171+1):
			self.start_urls.append("http://bbs.rong360.com/forum-55-%d.html"%page)

	def parse(self, response):
		urls = response.xpath('//tbody[contains(@id, "normalthread")]/tr/td[@class="icn"]/a/@href').extract()
		for url in urls:
			df = open("urls.txt", "a")
			df.write(url+"\n")
			df.close()

