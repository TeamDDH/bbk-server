# -*- coding: utf-8 -*-
"""
    pipelines
    ~~~~~~~~~

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from scrapy.exceptions import DropItem
from .db import spider_session_generator, RawArticle


class ArticlePipeline(object):
    """Persist article items into database."""

    def __init__(self):
        self.spider_session_generator = spider_session_generator

    def process_item(self, item, spider):
        if item.get('title', None) is None:
            raise DropItem('Article doesn\'t have a title.')
        else:
            title = item.get('title')[0]
            if title:
                title = title.strip()

            uri = item.get('uri')[0]
            content = item.get('content')[0]
            if content:
                content = content.strip()

            source = item.get('source')[0]
            crawled_at = item.get('crawled_at')[0]
            # published_at = item.get('published_at')[0]
            # editor = item.get('editor')[0]
            # published_time = item.get('published_time')[0]

            if title is None or title == '' or content is None or content == '':
                raise DropItem('Article doesn\'t have valid information.')

            session = self.spider_session_generator()
            session.add(RawArticle(title=title, uri=uri, source=source,
                                   crawled_at=crawled_at, content=content))
            session.commit()
            session.close()

            #: return the item for any other after-processing
        return item
