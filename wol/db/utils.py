from . import Base, engine


def create_tables():
    """
    Creates all DB tables based on meta object
    """
    Base.metadata.create_all(engine)

