from sqlalchemy import Column, String, create_engine, Integer, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from shared.config import SPIDER_DATABASE_URI

# create ORM to spider database
SpiderBase = declarative_base()
spider_engine = create_engine(SPIDER_DATABASE_URI)
spider_session_generator = sessionmaker(bind=spider_engine)


class RawArticle(SpiderBase):
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


SpiderBase.metadata.create_all(bind=spider_engine)
