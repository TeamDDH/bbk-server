# -*- coding: utf-8 -*-
"""
    models.subscription
    ~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from ..util.datetime import get_current_timestamp
from ..exts import db


class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    topic_id = db.Column(db.Integer,
                         db.ForeignKey('topics._id'),
                         primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users._id'),
                        primary_key=True)
    created_datetime = db.Column(db.BigInteger)
    topic = db.relationship('Topic', back_populates='subscribers')
    subscriber = db.relationship('User', back_populates='subscribed_topics')

    def __int__(self, topic_id, user_id):
        self.topic_id = topic_id
        self.user_id = user_id
        self.created_datetime = get_current_timestamp()

    @classmethod
    def register_subscription(cls, user_id, topic_id):
        subscription = cls(topic_id=topic_id, user_id=user_id)
        db.session.add(subscription)
        db.session.commit()
        return subscription

    @classmethod
    def remove_subscription(cls, user_id, topic_id):
        try:
            subscription = cls.get_subscription(user_id, topic_id)
            db.session.delete(subscription)
            db.session.commit()
            return True
        except IOError as e:
            print e
            return False

    @classmethod
    def get_subscription_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_subscription(cls, user_id, topic_id):
        return cls.query.filter_by(user_id=user_id, topic_id=topic_id).first()

    def __repr__(self):
        return '<Subscription> user_id: %d, topic_id: %d' % (self.user_id,
                                                             self.topic_id)
