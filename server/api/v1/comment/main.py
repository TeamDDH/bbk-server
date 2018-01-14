# -*- coding: utf-8 -*-
"""
    api.v1.comment.main
    ~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from flask_restful import Resource, abort, marshal

from server.models import Comment
from server.exts.login_manager import login_required, current_user
from .parser import (get_comment_parser,
                     post_comment_parser,
                     delete_comment_parser)
from .field import (comment_to_article_field,
                    comment_object_field,
                    sub_comment_object_field)
from ..article.main import get_article_or_404


def get_comment_or_404(comment_id):
    ret = Comment.get_by_id(comment_id)
    if not ret:
        abort(404)
    return ret


def get_comments_by_article_id(article_id):
    ret = Comment.get_by_article_id(article_id)
    return ret


def store_comment(article_id, content, user):
    return Comment.create_comment(article_id, user._id, content)


def store_sub_comment(article_id, content, user, parent_id):
    return Comment.create_comment(article_id, user._id, content, True,
                                  parent_id)


def delete_comment(comment):
    return Comment.delete_comment(comment._id)


class CommentApi(Resource):
    def get(self):
        args = get_comment_parser.parse_args()
        _id = args['_id']
        article_id = args['article_id']

        if _id and article_id:
            abort(400,
                  message='_id and article_id cannot be passed at same time.')

        if _id:
            return marshal(get_comment_or_404(_id), comment_object_field)

        if article_id:
            comments = get_comments_by_article_id(article_id)
            return marshal(comments, comment_to_article_field)

    @login_required
    def post(self):
        """Upload a new comment or sub comment to server."""
        args = post_comment_parser.parse_args()
        article_id = args['article_id']

        get_article_or_404(article_id)
        #: if article doesn't exist, there's no need to deal with this request

        content = args['content']
        is_sub = args['is_sub']
        parent_id = args['parent_id']
        user = current_user  #
        #: safe to use `current_user` in `login_required` protected methods

        if is_sub and parent_id:
            comment = store_sub_comment(article_id, content, user, parent_id)
            return marshal(comment, sub_comment_object_field)

        if not is_sub:
            comment = store_comment(article_id, content, user)
            return marshal(comment, comment_object_field)

    @login_required
    def delete(self):
        """Delete a comment."""
        args = delete_comment_parser()
        _id = args['_id']
        comment = get_comment_or_404(_id)
        user = current_user

        if comment.user_id != user._id:
            abort(401, message='Comment uploader is not current user.')

        flag = delete_comment(comment)
        if flag:
            return 204
        else:
            abort(500)
