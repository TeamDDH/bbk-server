# -*- coding: utf-8 -*-
"""
    app
    ~~~

    This module provides a factory function to create application.

    :copyright: (c) 2017 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from flask import Flask

from config import configs
from .api.v1 import api_v1
from .exts import db
from .exts.login_manager import Manager


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(configs[config_name])

    #: register blueprints
    app.register_blueprint(api_v1, url_prefix='/v1')

    #: initialize extensions
    db.init_app(app)
    login_manager = Manager()
    login_manager.init_app(app)

    return app
