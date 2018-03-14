# -*- coding: utf-8 -*-
"""
    api.v1.topic.parser
    ~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""


from flask_restful import reqparse

get_topic_parser = reqparse.RequestParser()
get_topic_parser.add_argument('_id', type=str)
get_topic_parser.add_argument('page_num', type=int)

post_topic_parser = reqparse.RequestParser()
post_topic_parser.add_argument('title',
                               type=str,
                               location='json')
