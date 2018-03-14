# -*- coding: utf-8 -*-
"""
    tencent_spider
    ~~~~~~~~~~~~~~

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

import scrapy
from scrapy.loader import ItemLoader

from spider.config import START_POINTS
from spider.items import ArticleItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    start_urls = START_POINTS['qq']

    def parse(self, response):
        pass

    def parse_article(self, response):
        loader = ItemLoader(item=ArticleItem(), response=response)
        loader.add_xpath('title', '')
        loader.add_xpath('content', '')
        loader.add_xpath('author', '')
        loader.add_xpath('uri', response.url)
        loader.add_value('source', 'tencent')
        return loader.load_item()
