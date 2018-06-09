# -*- coding: utf-8 -*-
"""
    utils
    ~~~~~

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

import redis

from shared.config import SPIDER_REDIS_CONFIG


class DuplicateChecker(object):
    """A simple Redis based existence checker."""

    def __init__(self):
        self.redis = redis.Redis(host=SPIDER_REDIS_CONFIG['host'],
                                 port=SPIDER_REDIS_CONFIG['port'],
                                 db=0)

    def write(self, values):
        self.redis.sadd('urls', values)

    def query(self, values):
        return self.redis.sismember('urls', values)
