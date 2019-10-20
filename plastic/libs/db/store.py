# -*- coding: utf-8 -*-

from sqlalchemy import create_engine

from plastic.config import SQLALCHEMY_DATABASE_URI

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, max_overflow=80, pool_size=100, pool_recycle=3600,
    isolation_level="AUTOCOMMIT"
)
db = engine.connect()
