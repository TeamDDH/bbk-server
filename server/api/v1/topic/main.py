# -*- coding: utf-8 -*-
"""
    api.v1.topic.main
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from flask_restful import Resource, marshal, abort

from server.exts.login_manager import superuser_required
from server.models import Topic
from .field import topic_object_field, topic_pagination_field
from .parser import get_topic_parser, post_topic_parser


def get_topic_or_404(topic_id):
    ret = Topic.get_by_id(topic_id)
    if not ret:
        abort(404, desc='Topic not found.')
    return ret


def get_topics_pagination(page_number):
    return Topic.get_pagination(page_number)


def create_topic(title):
    return Topic.create_topic(title)


class TopicApi(Resource):
    def get(self):
        """Get topic/topics by:.
        1. _id (topic_id)
        2. NO PARAM (in pagination form)
        """
        args = get_topic_parser.parse_args()
        _id = args['_id']
        page_num = args['page_num']

        if _id:
            return marshal(get_topic_or_404(_id), topic_object_field)
        if not _id and page_num:
            topic_pagination = get_topics_pagination(page_num)
            return marshal(topic_pagination, topic_pagination_field)

        abort(400, message='Bad parameters.')

    @superuser_required
    def post(self):
        """Create a topic.
        Preserved for development.
        """
        args = post_topic_parser.parse_args()
        title = args['title']

        new_topic = create_topic(title)
        return marshal(new_topic, topic_object_field), 201
