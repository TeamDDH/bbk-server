# -*- coding: utf-8 -*-
"""
    api.v1.user.field
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from flask_restful import fields

user_object_field = {
    '_id': fields.Integer,
    'email': fields.String,
    'phone_number': fields.String,
    'username': fields.String,
    'avatar_url': fields.String,
    'nickname': fields.String,
    'self_introduction': fields.String
}

user_list_field = {
    'users': fields.List(fields.Nested(user_object_field))
}

token_field = {
    'token': fields.String,
    'expire': fields.Integer,
    'user': fields.Nested(user_object_field)
}
