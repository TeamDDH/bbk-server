# -*- coding: utf-8 -*-
"""
    pipelines
    ~~~~~~~~~

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from scrapy.exceptions import DropItem
from .db import session_generator, Article


class ArticlePipeline(object):
    """Persist article items into database."""

    def __init__(self):
        self.session_generator = session_generator

    def process_item(self, item, spider):
        if item.get('title', None) is None:
            raise DropItem('Article doesn\'t have a title.')
        else:
            title = item.get('title')[0]
            uri = item.get('uri')[0]

            session = self.session_generator()
            session.add(Article(title=title, uri=uri))
            session.commit()
            session.close()

        #: return the item for any other after-processing
        return item
