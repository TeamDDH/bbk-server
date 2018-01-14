# -*- coding: utf-8 -*-
"""
    api.v1.auth.main
    ~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from flask import current_app
from flask_restful import Resource, marshal_with, abort

from server.models import User
from server.exts.login_manager import login_user
from .field import token_field
from .parser import login_parser


def get_user_or_404(username):
    ret = User.get_by_username(username)
    if not ret:
        abort(404, desc='User not found.')
    return ret


def try_login_user(user, password):
    if user.verify_password(password):
        return login_user(user)
    else:
        abort(403, message='Password is not correct or has been changed.')


class AuthApi(Resource):
    @marshal_with(token_field)
    def post(self):
        """Login user via this API. This API returns a token with which
        clients can authenticate.
        """
        args = login_parser.parse_args()
        username = args['username']
        password = args['password']

        user = get_user_or_404(username)
        token = try_login_user(user, password)
        ret = {
            'expire': current_app.config['AUTH_TOKEN_EXPIRE'],
            'token': token,
            'user': user
        }
        return ret, 201
