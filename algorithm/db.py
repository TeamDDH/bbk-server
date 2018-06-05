# -*- coding: utf-8 -*-
"""
    db
    ~~

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

import os

from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .config import SPIDER_DATABASE_URI

Base = declarative_base()
engine = create_engine(SPIDER_DATABASE_URI)
session_generator = sessionmaker(bind=engine)


class Article(Base):
    """Similar to the ORM mapping in server.models package, but these articles
    are just for the algorithm module. Maybe the database may be switched to
    another one.
    """
    __tablename__ = 'articles'

    _id = Column(Integer(), primary_key=True)
    title = Column(String(256), index=True)
    uri = Column(String(256))
    source = Column(String(128), nullable=True)
    created_at = Column(String(128), nullable=True)
    crawed_at = Column(String(128), nuillable=True)
    content = Column(String(256), nullable=True)
    editor = Column(String(128), nullable=True)
    published_at =Column (String(128), nullable=True)
    time = Column(date(), nuillable=True)
    keyword = Column(String(128))


Base.metadata.create_all(bind=engine)
