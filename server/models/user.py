# -*- coding: utf-8 -*-
"""
    models.user
    ~~~~~~~~~~~

    :copyright: (c) 2017 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from datetime import datetime
from flask import current_app
from itsdangerous import (TimedJSONWebSignatureSerializer as TSerializer,
                          BadSignature,
                          SignatureExpired)
from werkzeug.security import generate_password_hash, check_password_hash
from server.exts import db
from .subscription import Subscription


class User(db.Model):
    __tablename__ = 'users'

    _id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, nullable=True, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(32),
                             index=True,
                             nullable=True,
                             unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    nickname = db.Column(db.String(64), index=True, nullable=True)
    self_introduction = db.Column(db.Text)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    register_datetime = db.Column(db.DateTime)
    last_login_datetime = db.Column(db.DateTime)
    is_confirmed = db.Column(db.Boolean, default=False)
    is_superuser = db.Column(db.Boolean, default=False)

    #: relationships to other models
    comments = db.relationship('Comment', backref='uploader', lazy='dynamic')
    subscribed_topics = db.relationship('Subscription',
                                        back_populates='subscriber')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def generate_auth_token(self, expiration=None):
        if expiration is None:
            expiration = current_app.config['AUTH_TOKEN_EXPIRE']
        s = TSerializer(current_app.config['AUTH_SECRET_KEY'],
                        expires_in=expiration)
        return s.dumps({'_id': self._id})

    @staticmethod
    def load_user_from_auth_token(token):
        s = TSerializer(current_app.config['AUTH_SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return False  #: overtime signature
        except BadSignature:
            return False  #: wrong signature
        user_id = data['_id']
        return User.get_by_id(user_id)

    @property
    def password(self):
        raise AttributeError('Password is not readable.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, email=None, phone_number=None, username=None,
                 password=None, is_superuser=False, nickname=None,
                 self_introduction=None, first_name=None, last_name=None):
        self.email = email
        self.phone_number = phone_number
        self.username = username
        self.password = password
        self.register_time = datetime.utcnow()
        self.last_login_time = datetime.utcnow()
        self.is_confirmed = False
        self.is_superuser = is_superuser
        self.nickname = nickname
        self.self_introduction = self_introduction
        self.first_name = first_name
        self.last_name = last_name

    @classmethod
    def create_user(cls, username, password):
        """Create a user, store and return it."""
        # TODO: support phone_number registration and login.
        new_user = cls(username=username, password=password, nickname=username)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(_id=int(user_id)).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def __repr__(self):
        return '<User> _id: %d, username: %s' % (self._id, self.username)
