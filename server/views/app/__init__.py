# -*- coding: utf-8 -*-
"""
    app
    ~~~

    The Vue web clinet of bbk.

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from flask import Blueprint


app = Blueprint('app', __name__)


@app.route('/')
def index():
    return 'Hello, BBK!'
