# -*- coding: utf-8 -*-
"""
    api.v1.comment.field
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from flask_restful import fields

nested_user_object_field = {
    '_id': fields.Integer,
    'username': fields.String,
    'avatar_url': fields.String,
    'nickname': fields.String,
}

sub_comment_object_field = {
    '_id': fields.Integer,
    'content': fields.String,
    'created_datetime': fields.Integer,
    'approve_count': fields.Integer,
    'disapprove_count': fields.Integer,
    'uploader': fields.Nested(nested_user_object_field)
}

comment_object_field = {
    '_id': fields.Integer,
    'content': fields.String,
    'created_datetime': fields.Integer,
    'approve_count': fields.Integer,
    'disapprove_count': fields.Integer,
    'uploader': fields.Nested(nested_user_object_field),
    'sub_comments': fields.List(fields.Nested(sub_comment_object_field))
}

comment_to_article_field = {
    'comments': fields.List(fields.Nested(comment_object_field))
}
