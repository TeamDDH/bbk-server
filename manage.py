# -*- coding: utf-8 -*-
"""
    manage
    ~~~~~~
    Script to manage this project.

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server, Shell

from server import create_server
from server.exts import db
from server.models import User, Article, Topic, Comment, Subscription

from algorithm import start_processing
from spider import start_spider

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


#: register my commands
@manager.command
def fake():
    for i in range(1, 10):
        title = 'Fake Topic # %d' % i
        Topic.create_topic(title=title)


@manager.command
def spider():
    start_spider()


@manager.command
def alg():
    start_processing()


if __name__ == '__main__':
    manager.run()
