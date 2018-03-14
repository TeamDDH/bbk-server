# -*- coding: utf-8 -*-
"""
    api.v1
    ~~~~~~

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from flask import Blueprint
import flask_restful as restful

from .article import ArticleApi
from .auth import AuthApi
from .user import UserApi
from .topic import TopicApi
from .subscription import SubscriptionApi

api_v1 = Blueprint('api_v1', __name__)
api = restful.Api(api_v1)

api.add_resource(ArticleApi, '/article')
api.add_resource(UserApi, '/user')
api.add_resource(AuthApi, '/auth')
api.add_resource(TopicApi, '/topic')
api.add_resource(SubscriptionApi, '/subscription')
