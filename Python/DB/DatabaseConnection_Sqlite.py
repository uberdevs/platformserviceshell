from sqlalchemy import create_engine

# create seperate class to prevent connection pool creation until we need it
class Database:
    # connection pool initially with 2 and a max of 20 connections to reuse
    # the __ makes this property private
    __connection = None
    __engine = None

    # once intialized this pool is shared across usages of the Databaseclass
    # no self since we use @classmethod so we use cls instead
    @classmethod
    def inialize(cls):
        # our sql lite db for our restful api shell
        # TODO  : remove the hard coded name for the db
        cls.__engine = create_engine('sqlite:///A:\\Work\\Python\\Vagrant\\api_server\\DB\\restaurants.db')
        return cls.__engine

    @classmethod
    def get_connection(cls):
        cls.__connection = cls.__engine.connect()
        return cls.__connection

class get_a_connection:
    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = Database.get_connection()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.connection.rollback()
        else:
            self.connection.commit()

