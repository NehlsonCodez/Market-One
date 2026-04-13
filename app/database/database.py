from sqlalchemy import create_engine
from sqlalchemy.dialects.sqlite import *
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./market.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": "false"})

session = sessionmaker(auto_commit = False, autoflush = False, bind = engine)

Base = declarative_base()