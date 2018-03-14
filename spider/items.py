# -*- coding: utf-8 -*-
"""
    items
    ~~~~~

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""


import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()  #: title of the article
    uri = scrapy.Field()  #: link to the article
    content = scrapy.Field()  #: the formatted content of the article
    author = scrapy.Field()
    source = scrapy.Field()  #: the website where the article if from
    published_at = scrapy.Field()
    crawled_at = scrapy.Field()
