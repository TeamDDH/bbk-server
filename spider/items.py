# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()  #: title of the article
    uri = scrapy.Field()  #: link to the article
    content = scrapy.Field()  #: the formatted content of the article
    author = scrapy.Field()
    source = scrapy.Field()  #: the website where the article if from
    published_at = scrapy.Field()
    crawled_at = scrapy.Field()
