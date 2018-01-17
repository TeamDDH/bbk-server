# -*- coding: utf-8 -*-
"""
    config
    ~~~~~~

    :copyright: (c) 2017 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

#: start points for spiders
#: also in `IgnoreDuplicatedRequestMiddleware`, scrapy would check if the
#: current request is in this list. if true, it wouldn't ignore it.
START_POINTS = [
    'http://www.sina.com.cn',
    'http://www.qq.com',
]

#: a list of websites
#: Sina
#: Tencent

#: database
SPIDER_DATABASE_URI = 'mysql://root:sige1995@localhost:3306/bbk'
SPIDER_REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6379,
}
