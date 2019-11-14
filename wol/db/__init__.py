from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from wol.settings import DB_PATH

Base = declarative_base()

engine = create_engine(DB_PATH, echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()
