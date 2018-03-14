# -*- coding: utf-8 -*-
"""
    exts
    ~~~~

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from flask_sqlalchemy import SQLAlchemy

from .login_manager import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
