# -*- coding: utf-8 -*-
"""
    sina_spider
    ~~~~~~~~~~~

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

import scrapy
from scrapy.loader import ItemLoader

from spider.config import START_POINTS
from spider.items import ArticleItem


class SinaSpider(scrapy.Spider):
    name = 'sina'
    start_urls = [START_POINTS['sina']]

    def parse(self, response):
        selectors = response.css('div.newslist ul.list-a > li > a')
        for s in selectors:
            #: follow links to articles
            # FIXME: not always a link to article
            #: TODO: track to another columns pages
            item = (s.xpath('@href').extract_first(),
                    s.css('a::text').extract_first())
            yield response.follow(item[0], callback=self.parse_article)

    def parse_article(self, response):
        """In this parser, a new article item would be created and
        in `pipeline.py` it would be stored into database."""
        loader = ItemLoader(item=ArticleItem(), response=response)
        loader.add_css('title', 'h1::text')
        loader.add_value('author', '')
        loader.add_value('uri', response.url)
        loader.add_value('source', 'sina')
        item = loader.load_item()
        yield item
