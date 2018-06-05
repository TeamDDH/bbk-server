# -*- coding: utf-8 -*-
"""
    spider
    ~~~~~~

    The spider module of bbk system.

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

#: expose a method to trigger scrabbling, required by Celery
# coding:utf-8

from scrapy import cmdline


def start_spider():
    # cmdline.execute("scrapy crawl cctv".split())
    # cmdline.execute("scrapy crawl chinadaily".split())
    cmdline.execute("scrapy crawl fenghuang".split())
    # cmdline.execute("scrapy crawl people".split())
    cmdline.execute("scrapy crawl sina".split())
