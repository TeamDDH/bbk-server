# -*- coding: utf-8 -*-
"""
    server
    ~~~~~~

    This module provides a factory function to create application.

    :copyright: (c) 2017 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from flask import Flask

from config import configs
from .api.v1 import api_v1
from .views.app import app
from .exts import db
from .exts.login_manager import Manager


def create_server(config_name):
    server = Flask(__name__)
    server.config.from_object(configs[config_name])

    #: register blueprints
    server.register_blueprint(api_v1, url_prefix='/v1')
    server.register_blueprint(app)

    #: initialize extensions
    db.init_app(server)
    login_manager = Manager()
    login_manager.init_app(server)

    return server
