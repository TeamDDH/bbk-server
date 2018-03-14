# -*- coding: utf-8 -*-
"""
    exts.login_manager
    ~~~~~~~~~~~~~~~~~~

    A simple authentication to load user information and set it to request
    context.

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

from functools import wraps
from flask import (_request_ctx_stack, has_request_context, request,
                   current_app)
from flask_restful import abort
from werkzeug.local import LocalProxy

#: a proxy for the current user
#: it would be an anonymous user if no user is logged in
current_user = LocalProxy(lambda: _get_user())


class AnonymousUserMixin(object):
    @property
    def is_active(self):
        return False

    @property
    def is_authenticated(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def __repr__(self):
        return '<AnonymousUser>'


class UserMixin(object):
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __repr__(self):
        return '<AuthenticatedUser>'


class LoginManager(object):
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.login_manager = self
        app.context_processor(_user_context_processor)

        self._anonymous_user = AnonymousUserMixin
        self._login_disabled = app.config['LOGIN_DISABLED'] or False
        self._cb = None

    def user_loader(self, cb):
        """register a callback to loader a unique user. This callback should
        receive a token and return a User object or None."""
        self._cb = cb
        return cb

    def _load_user(self):
        """Try to load user from request.json.token and set it to
        `_request_ctx_stack.top.user`. If None, set current user as an
        anonymous user.
        """

        ctx = _request_ctx_stack.top
        json = request.json
        user = self._anonymous_user()

        if json and json.get('token') and this._cb is not None:
            real_user = this._cb(json.get('token'))
            if real_user:
                user = real_user

        ctx.user = user


def _get_user():
    """Get current user from request context."""
    if has_request_context() and not hasattr(_request_ctx_stack.top, 'user'):
        current_app.login_manager._load_user()

    return getattr(_request_ctx_stack.top, 'user', None)


def _user_context_processor():
    """A context processor to prepare current user."""
    return dict(current_user=_get_user())


def login_user(user):
    """Login a user and return a token."""
    _request_ctx_stack.top.user = user
    return user.generate_auth_token()


def logout_user(user):
    """For a restful API there shouldn't be a `logout` method because the
    server is stateless.
    """
    pass


def login_required(func):
    """Decorator to protect view functions that should only be accessed
    by authenticated users.
    """

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            abort(403, message='Please login before carrying out this action.')
        return func(*args, **kwargs)

    return decorated_view


def anonymous_required(func):
    """Decorator to protect view functions that should only be accessed
    by unauthenticated users."""

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated:
            abort(400, message='Not available now.')
        return func(*args, **kwargs)

    return decorated_view


def superuser_required(func):
    """Decorator protect view functions that should only be accessed by
    superusers. This is a very naive mechanism to check authorization, and
    currently not used in this project.
    """

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_superuser:
            abort(401, message='You are not admin.')
        return func(*args, **kwargs)

    return decorated_view
