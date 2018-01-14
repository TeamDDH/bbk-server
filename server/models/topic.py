# -*- coding: utf-8 -*-
"""
    models.topic
    ~~~~~~~~~~~~

    :copyright: (c) 2017 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from datetime import datetime
from ..exts import db


class Topic(db.Model):
    __tablename__ = 'topics'

    _id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True)
    created_datetime = db.Column(db.DateTime)
    updated_datetime = db.Column(db.DateTime)

    #: relationships to other models
    articles = db.relationship('Article', backref='topic', lazy='dynamic')
    subscribers = db.relationship('Subscription',
                                  back_populates='topic')

    def __init__(self, title):
        self.title = title
        self.created_datetime = datetime.utcnow()
        self.updated_datetime = datetime.utcnow()

    #: create methods
    @classmethod
    def create_topic(cls, title):
        new_topic = cls(title)
        db.session.add(new_topic)
        db.session.commit()
        return new_topic

    #: get methods
    @classmethod
    def get_by_id(cls, topic_id):
        return cls.query.filter_by(_id=int(topic_id)).first()

    @classmethod
    def get_pagination(cls, page_number, per_page=20):
        return cls.query \
            .order_by(Topic.created_datetime.desc()) \
            .paginate(page=page_number, per_page=per_page, error_out=False)

    def __repr__(self):
        return '<Topic Object> _id: %d, title: %s.' % (self._id, self.title)
