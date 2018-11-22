# -*- coding: utf-8 -*-
import scrapy

from Report.items import ReportItem
from scrapy.http import Request


class ReportSpider(scrapy.Spider):
    # 定义爬虫的名字和需要爬取的网址
    name = 'report'
    allowed_domains = ['www.abckg.com']
    start_urls = ['http://www.abckg.com/']

    def parse(self, response):
        for r in response.css('.post'):
            # 实例化item
            item = ReportItem()
            # 把获得到的内容保存到item内
            item['href'] = r.css('h2 a::attr(href)').extract()
            item['title'] = r.css('h2 a::text').extract()
            item['content'] = r.css('.intro p::text').extract()
            yield item

        # 下面是多页面的爬取方法
        urls = response.css('pageinfo a::attr(href)').extract()
        for url in urls:
            yield Request(url, callback=self.parse)
        categorys = response.css('.menu li a::attr(href)').extract()
        for ct in categorys:
            yield Request(ct, callback=self.parse)
