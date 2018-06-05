# -*- coding: utf-8 -*-
"""
    tasks
    ~~~~~

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

import time
from scrapy import log, signals
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from celery import Celery
from spider.spiders.sina_spider import SinaSpider

CELERY_DATABASE_URI = 'redis://localhost:6379/0'
CELERY_BROKER_URL = ''


CELERY_SCHEDULE = {
    'hourly-digest': {
        'task': 'tasks.run_spider',
        # FIXME: change it to every hour
        'schedule': contrab(day_of_week, hour='')
    }
}

celery = Celery('tasks', broker=CELERY_DATABASE_URI, backend=)


@celery.task
def run_spider():
    return x + y
