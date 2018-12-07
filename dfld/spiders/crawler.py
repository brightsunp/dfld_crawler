# -*- coding: utf-8 -*-
import scrapy
from ..items import DfldItem


class CrawlerSpider(scrapy.Spider):
    name = 'crawler'
    allowed_domains = ['ldzl.people.com.cn']
    start_urls = ['http://ldzl.people.com.cn/dfzlk/front/firstPage.htm']

    def parse(self, response):
        for link in response.css('a::attr(href)').extract():
            if 'personProvince' in link:
                yield scrapy.Request(response.urljoin(link), callback=self.parse)
            if 'personPage' in link:
                yield scrapy.Request(response.urljoin(link), callback=self.page_parse)

    def page_parse(self, response):
        item = DfldItem()
        item['url'] = response.url
        item['title'] = response.css('title::text').extract_first()
        item['content'] = response.body.decode(response.encoding)
        yield item
