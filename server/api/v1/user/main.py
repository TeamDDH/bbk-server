# -*- coding: utf-8 -*-
"""
    api.v1.user.main
    ~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from flask import current_app
from flask_restful import Resource, abort, marshal, marshal_with

from server.exts.login_manager import login_user, anonymous_required
from server.models import User
from .field import user_object_field, token_field
from .parser import get_user_parser, register_parser


def get_user_by_username_or_error(username):
    user = User.get_by_username(username)
    if not user:
        abort(404, message='User not found.')
    return user


def get_user_by_id_or_404(user_id):
    user = User.get_by_id(user_id)
    if not user:
        abort(404, message='User not found.')
    return user


def create_user_or_error(username, password):
    if User.get_by_username(username):
        abort(400, message='Username already registered.')
    return User.create_user(username, password)


class UserApi(Resource):
    def get(self):
        """Get a user's information with user_id or username."""
        args = get_user_parser.parse_args()
        _id = args['_id']
        username = args['username']

        if _id and username:
            abort(401, message='_id and username cannot '
                               'be passed at the same time.')
        if _id and not username:
            user = get_user_by_id_or_404(_id)
            return marshal(user, user_object_field)
        if not _id and username:
            user = get_user_by_username_or_error(username)
            return marshal(user, user_object_field)
        if not _id and not username:
            abort(400, message='one of _id and username is required.')

    @anonymous_required
    @marshal_with(token_field)
    def post(self):
        """Sign up a new user. This API returns a token with which
        clients can authenticate and the newly created user's info.
        """
        args = register_parser.parse_args()
        username = args['username']
        password = args['password']

        new_user = create_user_or_error(username, password)
        token = login_user(new_user)
        ret = {
            'expire': current_app.config['AUTH_TOKEN_EXPIRE'],
            'token': token,
            'user': new_user
        }
        return ret, 201

    def delete(self):
        """Deactivate a user account. This service is not (and will not be)
        implemented.
        """
        return '', 204
