# -*- coding: utf-8 -*-
"""
    api.v1.article.main
    ~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from flask_restful import Resource, abort, marshal

from server.exts.login_manager import superuser_required
from server.models import Article
from .field import article_object_field, article_pagination_field
from .parser import get_article_parser, post_article_parser
from ..topic.main import get_topic_or_404


def get_article_or_404(article_id):
    ret = Article.get_by_id(article_id)
    if ret is None:
        abort(404, message='Article not found.')
    return ret


def get_pagination_in_topic(topic_id, page_number):
    topic = get_topic_or_404(topic_id)
    if topic:
        return Article.get_pagination_by_topic_id(topic_id, page_number)


def try_create_new_article(title, topic_id, uri):
    topic = get_topic_or_404(topic_id)
    new_article = Article.create_article(title, uri, topic_id)
    topic.articles.append(new_article)
    return new_article


class ArticleApi(Resource):
    def get(self):
        """Get an article / articles by:
        1. _id (article_id)
        2. topic_id (in pagination form)
        """
        args = get_article_parser.parse_args()
        _id = args['_id']
        topic_id = args['topic_id']
        page_num = args['page_num']

        #: if _id is provided, process the req regardless of other parameters
        if _id:
            return marshal(get_article_or_404(_id), article_object_field)

        #: if _id is not provided
        if not _id and topic_id and page_num:
            article_pagination = get_pagination_in_topic(topic_id, page_num)
            return marshal(article_pagination, article_pagination_field)

        abort(400, message='Bad arguments.')

    @superuser_required
    def post(self):
        """Create an article on server."""
        args = post_article_parser.parse_args()
        title = args['title']
        topic_id = args['topic_id']
        uri = args['uri']

        new_article = try_create_new_article(title, topic_id, uri)
        return marshal(new_article, article_object_field), 201
