# -*- coding: utf-8 -*-
"""
    server
    ~~~~~~

    This module provides a factory function to create application.

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from flask import Flask

from config import configs
from .api.v1 import api_v1
from .exts import db
from .exts.login_manager import LoginManager


def create_server(config_name):
    server = Flask(__name__)

    #: load configurations
    server.config.from_object(configs[config_name])

    #: register blueprints
    #: API v1.0
    server.register_blueprint(api_v1, url_prefix='/v1')

    #: initialize extensions
    db.init_app(server)

    #: self-writen plugins should be loaded after third-party plugins are
    #: loaded to avoid circle import
    login_manager = LoginManager(app=server)

    return server
