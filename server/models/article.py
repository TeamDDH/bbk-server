# -*- coding: utf-8 -*-
"""
    models.article
    ~~~~~~~~~~~~~~

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from shared.util import get_current_timestamp
from ..exts import db


class Article(db.Model):
    __tablename__ = 'articles'

    _id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True)
    uri = db.Column(db.String(256))
    content = db.Column(db.Text, nullable=True)
    author = db.Column(db.String(64), nullable=True)
    source = db.Column(db.String(128), nullable=True)
    created_datetime = db.Column(db.BigInteger)
    updated_datetime = db.Column(db.BigInteger)

    #: relationships to other models
    topic_id = db.Column(db.Integer, db.ForeignKey('topics._id'))
    comments = db.relationship('Comment', backref='article', lazy='dynamic')

    def __init__(self, title, uri, topic_id, content=None,
                 author=None, source=None):
        self.title = title
        self.uri = uri
        self.content = content
        self.author = author
        self.source = source
        self.created_datetime = get_current_timestamp()
        self.updated_datetime = get_current_timestamp()
        self.topic_id = topic_id

    #: create methods
    @classmethod
    def create_article(cls, title, uri, topic_id):
        new_article = cls(title, uri, topic_id)
        db.session.add(new_article)
        db.session.commit()
        return new_article

    #: get methods
    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, article_id):
        return cls.query.filter_by(_id=int(article_id)).first()

    @classmethod
    def get_by_topic_id(cls, topic_id):
        return cls.query.filter_by(topic_id=topic_id).all()

    @classmethod
    def get_pagination_by_topic_id(cls, topic_id, page_number, per_page=20):
        return cls.query \
            .filter_by(topic_id=topic_id) \
            .paginate(page=page_number, per_page=per_page, error_out=False)

    def __repr__(self):
        return '<Article Object> _id: %d, title: %s.' % (self._id, self.title)
