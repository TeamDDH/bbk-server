# -*- coding: utf-8 -*-
"""
    server
    ~~~~~~

    This module provides a factory function to create application.

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from flask import Flask

from .config import configs
from .api.v1 import api_v1
from .exts import db, login_manager
from .models.user import User


def create_server(config_name):
    server = Flask(__name__)

    #: load configurations
    server.config.from_object(configs[config_name])

    #: register blueprints
    #: API v1.0
    server.register_blueprint(api_v1, url_prefix='/v1')

    #: initialize extensions
    db.init_app(server)
    login_manager.init_app(server)

    #: register user loader for login_manager module
    @login_manager.user_loader
    def load(token):
        return User.load_user_from_auth_token(token)

    return server
