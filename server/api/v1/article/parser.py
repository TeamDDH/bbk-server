# -*- coding: utf-8 -*-
"""
    api.v1.article.parser
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from flask_restful import reqparse

get_article_parser = reqparse.RequestParser()
get_article_parser.add_argument('_id', type=int)
get_article_parser.add_argument('topic_id', type=int)
get_article_parser.add_argument('page_num', type=int)

post_article_parser = reqparse.RequestParser()
post_article_parser.add_argument('title', type=str, required=True)
post_article_parser.add_argument('uri', type=str, required=True)
post_article_parser.add_argument('topic_id', type=int, required=True)
