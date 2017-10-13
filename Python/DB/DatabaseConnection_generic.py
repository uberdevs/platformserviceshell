import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


def __init__(self, flavor, host, database, username, password):
    """
    flavor      str    the connector to use for SQLAlchemy (http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html#database-urls)
    host        str    the server IP or domain name to connect to
    database    str    the name of the database to connect to
    username    str    the username to connect to the database with
    password    str    the password to connect to the database with
    """

    engine = sqlalchemy.create_engine \
        ("{flavor}://{username}:{password}@{host}/{database}".format(flavor=flavor, host=host, database=database, username=username, password=password))
    Base.metadata.create_all(engine)
    self.session = sqlalchemy.orm.sessionmaker(bind=self.db)()
