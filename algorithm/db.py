# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, create_engine, Integer, Text, BigInteger, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from shared.config import SPIDER_DATABASE_URI, SERVER_DATABASE_URI
from shared.util import get_current_timestamp

SpiderBase = declarative_base()
spider_engine = create_engine(SPIDER_DATABASE_URI)
spider_session_generator = sessionmaker(bind=spider_engine)


class SpiderArticle(SpiderBase):
    """Similar to the ORM mapping in server.models package, but these articles
    are just for the algorithm module. Maybe the database may be switched to
    another one.
    """
    __tablename__ = 'articles'

    _id = Column(Integer(), primary_key=True)
    title = Column(String(256), index=True)
    uri = Column(String(256))
    content = Column(Text())
    source = Column(String(128))
    crawled_at = Column(String(128), nullable=True)
    published_at = Column(String(128), nullable=True)
    editor = Column(String(128), nullable=True)
    published_time = Column(String(128), nullable=True)

    @classmethod
    def get_all_articles(cls):
        session = spider_session_generator()
        articles = session.query(cls).all()
        session.close()
        return articles


# create ORM to server database
ServerBase = declarative_base()
server_engine = create_engine(SERVER_DATABASE_URI)
server_session_generator = sessionmaker(bind=server_engine)


class ServerArticle(ServerBase):
    __tablename__ = 'articles'

    _id = Column(Integer, primary_key=True)
    title = Column(String(256), index=True)
    uri = Column(String(256))
    content = Column(Text(), nullable=True)
    author = Column(String(64), nullable=True)
    source = Column(String(128), nullable=True)
    created_datetime = Column(BigInteger)
    updated_datetime = Column(BigInteger)

    topic_id = Column(Integer, ForeignKey('topics._id'))

    def __init__(self, title, uri, topic_id, content=None,
                 author=None, source=None):
        self.title = title
        self.uri = uri
        self.content = content
        self.author = author
        self.source = source
        self.topic_id = topic_id
        self.created_datetime = get_current_timestamp()
        self.updated_datetime = get_current_timestamp()

    @classmethod
    def insert_an_article(cls, title, uri, topic_id):
        new_article = cls(title, uri, topic_id)

        session = server_session_generator()
        session.add(new_article)
        session.commit()
        session.close()


class ServerTopic(ServerBase):
    __tablename__ = 'topics'

    _id = Column(Integer, primary_key=True)
    title = Column(String(256), index=True)
    created_datetime = Column(BigInteger)
    updated_datetime = Column(BigInteger)

    def __init__(self, title):
        self.title = title
        self.created_datetime = get_current_timestamp()
        self.updated_datetime = get_current_timestamp()

    @classmethod
    def insert_a_topic(cls, title):
        new_topic = cls(title)

        session = server_session_generator()
        session.add(new_topic)
        session.commit()
        session.refresh(new_topic)
        session.close()

        return new_topic


#: initialize all databases here
SpiderBase.metadata.create_all(bind=spider_engine)
ServerBase.metadata.create_all(bind=server_engine)
