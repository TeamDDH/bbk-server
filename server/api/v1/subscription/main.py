# -*- coding: utf-8 -*-
"""
    api.v1.subscription.main
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from flask_restful import Resource, marshal, abort

from server.exts.login_manager import login_required, current_user
from server.models import Subscription
from .parser import post_subscription_parser, get_subscription_parser
from .field import subscription_object_field
from ..user.main import get_user_by_id_or_404
from ..topic.main import get_topic_or_404
from ..topic.field import topic_list_field


def get_subscription_or_404(user, topic):
    subscription = Subscription.get_subscription(user._id, topic._id)
    if not subscription:
        abort(404, message='Not registered to the topic.')
    return subscription


def get_subscribed_topics(user_id):
    """Get topics that a user subscribed."""
    user = get_user_by_id_or_404(user_id)
    subscriptions = user.subscribed_topics
    #: unwrap subscription objects
    topics = []
    for sub in subscriptions:
        topics.append(sub.topic)
    return topics


class SubscriptionApi(Resource):
    def get(self):
        args = get_subscription_parser.parse_args()
        user_id = args['user_id']

        ret = {'topics': get_subscribed_topics(user_id)}
        return marshal(ret, topic_list_field)

    @login_required
    def post(self):
        args = post_subscription_parser.parse_args()
        topic_id = args['topic_id']
        user_id = current_user._id
        get_topic_or_404(topic_id)

        if Subscription.get_subscription(user_id, topic_id):
            abort(400, message='Topic already registered.')

        subscription = Subscription.register_subscription(user_id, topic_id)
        return marshal(subscription, subscription_object_field), 201

    @login_required
    def delete(self):
        args = post_subscription_parser.parse_args()
        topic_id = args['topic_id']
        user_id = current_user._id
        get_topic_or_404(topic_id)

        if not Subscription.get_subscription(user_id, topic_id):
            abort(400, message='Topic not subscribed.')

        if Subscription.remove_subscription(user_id, topic_id):
            return '', 204
        else:
            return '', 500
