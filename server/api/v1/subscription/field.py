# -*- coding: utf-8 -*-
"""
    api.v1.subscription.field
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from flask_restful import fields

subscription_object_field = {
    'topic_id': fields.Integer,
    'user_id': fields.Integer,
    'created_datetime': fields.Integer
}
