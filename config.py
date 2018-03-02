# -*- coding: utf-8 -*-
"""
    config
    ~~~~~~

    Configurations to the server.

    :copyright: (c) 2017 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

#: database uri
DEV_DB_URI = 'mysql+pymysql://root:sige1995@localhost:3306/bbkserver'
TEST_DB_URI = None
PROD_DB_URI = None  #: maybe I am not going to use prod mode on my mac...

#: secret key
DEV_SECRET_KEY = 'secretkeyfordev'
PROD_SECRET_KEY = os.getenv('BBK_SECRET_KEY') or None


class Config(object):
    #: security & authentication
    AUTH_SECRET_KEY = PROD_SECRET_KEY or DEV_SECRET_KEY
    AUTH_TOKEN_EXPIRE = 3600 * 24 * 30 * 6  #: half a year

    #: if true, all user would be recognized as authenticated
    LOGIN_DISABLED = False

    #: database
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_PROFILER_ENABLED = True

    #: error
    ERROR_404_HELP = False  #: suppress default 404 error message


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = DEV_DB_URI


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = TEST_DB_URI


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = PROD_DB_URI


configs = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
