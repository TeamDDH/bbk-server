# -*- coding: utf-8 -*-
"""
    api.v1.article.field
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from flask_restful import fields

article_object_field = {
    '_id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'created_datetime': fields.DateTime,
    'updated_datetime': fields.DateTime,
    'author': fields.String,
    'uri': fields.String,
    'source': fields.String,
    'topic_id': fields.Integer
}

article_list_field = {
    'articles': fields.List(fields.Nested(article_object_field))
}

article_pagination_field = {
    'articles': fields.List(fields.Nested(article_object_field),
                            attribute='items'),
    'current_page': fields.Integer,
    'has_prev': fields.Boolean,
    'prev_num': fields.Integer,
    'has_next': fields.Boolean,
    'next_num': fields.Integer,
    'last_page': fields.Integer,
    'pages': fields.Integer,
    'total': fields.Integer
}
