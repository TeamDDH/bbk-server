# -*- coding: utf-8 -*-
"""
    spider
    ~~~~~~

    The spider module of bbk system.

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders import SinaSpider, ChinadailySpider, FenghuangSpider, PeopleSpider, CCTVSpider


def start_spider():
    print '[INFO] running spiders'
    process = CrawlerProcess(get_project_settings())
    process.crawl(SinaSpider)
    process.crawl(ChinadailySpider)
    process.crawl(FenghuangSpider)
    process.crawl(PeopleSpider)
    process.crawl(CCTVSpider)
    process.start()

