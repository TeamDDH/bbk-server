# -*- coding: utf-8 -*-
"""
    api.v1.user.parser
    ~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from flask_restful import reqparse

get_user_parser = reqparse.RequestParser()
get_user_parser.add_argument('_id', type=str, location='args')
get_user_parser.add_argument('username', type=str, location='args')

register_parser = reqparse.RequestParser(bundle_errors=True)
register_parser.add_argument('username', type=str, required=True,
                             location='json',
                             help='username must be included and in json.')
register_parser.add_argument('password', type=str, required=True,
                             location='json',
                             help='password must be included and in json.')
