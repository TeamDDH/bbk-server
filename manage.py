# -*- coding: utf-8 -*-
"""
    manage
    ~~~~~~

    Script to manage server domestically.

    :copyright: (c) 2017 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server, Shell, prompt_bool

from server import create_server
from server.exts import db
from server.models import User, Article, Topic, Comment, Subscription

server = create_server(os.getenv('BBK_SERVER_ENV') or 'development')
manager = Manager(server)
migrate = Migrate(server, db)


def make_shell_context():
    """Make references in shell interactive context."""
    return dict(server=server,
                db=db,
                User=User,
                Article=Article,
                Topic=Topic,
                Comment=Comment,
                Subscription=Subscription)


#: register commands
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('server', Server)


@manager.command
def create_db():
    if prompt_bool('[WARNING] This will initialize the database. '
                   'Are you sure there is no database now?'):
        try:
            db.create_all()
            print '[INFO] Database created.'
        except IOError:
            print '[ERROR] Failed! Maybe you have initialized the database.'
    else:
        print '[INFO] We are not going to create database.'


if __name__ == '__main__':
    manager.run()
