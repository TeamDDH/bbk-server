# -*- coding: utf-8 -*-
"""
    celerier
    ~~~~~~~~

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

import time

from scrapy import log, signals
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from celery import Celery

from spider.spiders.sina_spider import SinaSpider


master = Celery('tasks', broker='redis://localhost:6379/0')


@master.task
def run_spider():
    return x + y
