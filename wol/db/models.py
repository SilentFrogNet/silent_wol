from sqlalchemy import Column, Integer, String

from . import Base


class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True, nullable=False)
    mac = Column(String(20), unique=True, nullable=False)
    net_name = Column(String(250), unique=True, nullable=True)
