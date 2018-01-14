# -*- coding: utf-8 -*-
"""
    api.v1.auth.parser
    ~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from flask_restful import reqparse

login_parser = reqparse.RequestParser()
login_parser.add_argument('username',
                          type=str,
                          location='json',
                          help='username must be included.')
login_parser.add_argument('password',
                          type=str,
                          location='json',
                          help='password must be included.')
