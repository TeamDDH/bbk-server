# -*- coding: utf-8 -*-
"""
    api.v1.comment.parser
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from flask_restful import reqparse

get_comment_parser = reqparse.RequestParser()
get_comment_parser.add_argument('_id', type=int)
get_comment_parser.add_argument('article_id', type=int)
get_comment_parser.add_argument('user_id', type=int)

post_comment_parser = reqparse.RequestParser()
post_comment_parser.add_argument('article_id', type=int, required=True)
post_comment_parser.add_argument('content', type=str, required=True)
post_comment_parser.add_argument('is_sub', type=bool, required=True)
post_comment_parser.add_argument('parent_id', type=int)

delete_comment_parser = reqparse.RequestParser()
delete_comment_parser.add_argument('_id', required=True)
