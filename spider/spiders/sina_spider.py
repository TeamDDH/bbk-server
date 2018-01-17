# -*- coding: utf-8 -*-
"""
    sina_spider
    ~~~~~~~~~~~

    :copyright: (c) 2017 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

import scrapy
from scrapy.loader import ItemLoader

from spider.items import ArticleItem


class SinaSpider(scrapy.Spider):
    name = 'sina'
    start_urls = [
        'http://www.sina.com.cn',
    ]

    def parse(self, response):
        selectors = response.css('div.newslist ul.list-a > li > a')
        for s in selectors:
            item = (s.xpath('@href').extract_first(),
                    s.css('a::text').extract_first())
            yield response.follow(item[0], callback=self.parse_article)

    def parse_article(self, response):
        loader = ItemLoader(item=ArticleItem(), response=response)
        loader.add_css('title', 'h1::text')
        loader.add_value('author', '')
        loader.add_value('uri', response.url)
        loader.add_value('source', 'sina')
        item = loader.load_item()
        yield item
