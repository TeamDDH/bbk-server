# -*- coding: utf-8 -*-
"""
    exts
    ~~~~

    All third-party flask extensions would be initialized here.
    :important: Do not include in-project extensions in this file.

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
