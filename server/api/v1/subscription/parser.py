# -*- coding: utf-8 -*-
"""
    api.v1.subscription.parser
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from flask_restful import reqparse

#: post_subscription_parser is an alias
post_subscription_parser = subscription_parser = reqparse.RequestParser()
subscription_parser.add_argument('topic_id',
                                 type=int,
                                 required=True,
                                 help='topic_id is required.')

get_subscription_parser = reqparse.RequestParser()
get_subscription_parser.add_argument('user_id',
                                     type=int,
                                     required=True,
                                     help='user_id is required.')
