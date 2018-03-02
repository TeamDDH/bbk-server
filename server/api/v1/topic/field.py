# -*- coding: utf-8 -*-
"""
    api.v1.topic.field
    ~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from flask_restful import fields

topic_object_field = {
    '_id': fields.Integer,
    'title': fields.String,
    'created_datetime': fields.Integer,
    'updated_datetime': fields.Integer,
    'desc': fields.String
}

topic_list_field = {
    'topics': fields.List(fields.Nested(topic_object_field))
}

topic_pagination_field = {
    'topics': fields.List(fields.Nested(topic_object_field),
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
