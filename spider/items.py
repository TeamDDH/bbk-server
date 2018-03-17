# -*- coding: utf-8 -*-
"""
    items
    ~~~~~

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""


import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    uri = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    source = scrapy.Field()
    published_at = scrapy.Field()
    crawled_at = scrapy.Field()
