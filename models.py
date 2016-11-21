from datetime import datetime
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import sessionmaker

import settings

Base = declarative_base()
Session = sessionmaker(bind=create_engine(URL(**settings.DATABASE)))


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class GameUser(Base):
    __tablename__ = 'game_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column('username', String, unique=True, nullable=False)
    user_created = Column('user_created', DateTime, default=datetime.utcnow)


class Resource(Base):
    __tablename__ = 'resource'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column('user_id', Integer, ForeignKey('game_user.id'), nullable=False)
    resource_type = Column('resource_type', String, nullable=False)
    amount = Column('amount', Integer, nullable=False)
    UniqueConstraint(user_id, resource_type)


class Building(Base):
    __tablename__ = 'building'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column('user_id', Integer, ForeignKey('game_user.id'), nullable=False)
    building_type = Column('building_type', String, nullable=False)
    storage_capacity = Column('storage_capacity', Integer, nullable=False)
    production_capacity = Column('production_capacity', Integer, nullable=False)
    created_at = Column('created_at', DateTime, default=datetime.utcnow)
    last_harvested_at = Column('last_harvested_at', DateTime, default=datetime.utcnow)
    last_upgraded_at = Column('last_upgraded_at', DateTime, default=datetime.utcnow)
    UniqueConstraint(user_id, building_type)

Base.metadata.create_all(db_connect())
