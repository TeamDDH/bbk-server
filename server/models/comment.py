# -*- coding: utf-8 -*-
"""
    models.comment
    ~~~~~~~~~~~~~~

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from shared.util import get_current_timestamp
from ..exts import db


class Comment(db.Model):
    __tablename__ = 'comments'

    _id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    created_datetime = db.Column(db.BigInteger)
    is_sub_comment = db.Column(db.Boolean)
    approve_count = db.Column(db.Integer)
    disapprove_count = db.Column(db.Integer)

    #: relationships to other models
    article_id = db.Column(db.Integer,
                           db.ForeignKey('articles._id'),
                           nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users._id'),
                        nullable=False)
    parent_comment_id = db.Column(db.Integer,
                                  db.ForeignKey('comments._id'),
                                  nullable=True)
    parent_comment = db.relationship('Comment',
                                     backref='child_comments',
                                     remote_side=[_id])

    @property
    def sub_comments(self):
        if not self.is_sub_comment:
            return []
        return None

    @sub_comments.setter
    def sub_comments(self, value):
        raise AttributeError('sub_comments cannot be set, '
                             'change child_comments instead.')

    def __init__(self, content, article_id, user_id, is_sub_comment=False,
                 parent_comment_id=None):
        self.content = content
        self.article_id = article_id
        self.is_sub_comment = is_sub_comment
        self.created_datetime = get_current_timestamp()
        self.user_id = user_id
        self.approve_count = 0
        self.disapprove_count = 0
        if is_sub_comment:
            self.parent_comment_id = parent_comment_id

    #: create methods
    @classmethod
    def create_comment(cls, article_id, user_id, content,
                       is_sub_comment=False, parent_comment_id=0):
        new_comment = cls(article_id=article_id,
                          user_id=user_id,
                          content=content,
                          is_sub_comment=is_sub_comment,
                          parent_comment_id=parent_comment_id)
        db.session.add(new_comment)
        db.session.commit()
        return new_comment

    #: get methods
    @classmethod
    def get_by_id(cls, article_id):
        return cls.query.filter_by(_id=article_id).first()

    #: delete methods
    @classmethod
    def delete_comment(cls, comment_id):
        comment_to_delete = cls.get_by_id(comment_id)
        try:
            if not comment_to_delete.is_sub_comment:
                for item in comment_to_delete.child_comments:
                    db.session.remove(item)
            db.session.remove(comment_to_delete)
            db.session.commit()
            return True
        except IOError as e:
            print e.message
            return False

    @classmethod
    def get_by_article_id(cls, article_id):
        return cls.query \
            .filter_by(article_id=article_id) \
            .order_by(cls.created_datetime) \
            .all()

    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_pagination_by_article_id(cls, article_id, page_num, per_page=10):
        return cls.query \
            .filter_by(article_id=article_id) \
            .paginate(page=page_num, per_page=per_page, error_out=False)

    @classmethod
    def get_pagination_by_user_id(cls, user_id, page_num, per_page=10):
        return cls.query \
            .filter_by(user_id=user_id) \
            .order_by(cls.created_datetime) \
            .paginate(page=page_num, per_page=per_page, error_out=False)

    def __repr__(self):
        return '<Comment> _id: %d, user_id: %d' % (self._id, self.user_id)
