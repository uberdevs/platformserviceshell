from sqlalchemy import create_engine

# create seperate class to prevent connection pool creation until we need it
class Database:
    __connection = None
    __engine = None

    @classmethod
    def inialize(cls):
        # our sql lite db for our restful api shell
        # TODO  : remove the hard coded name for the db
        cls.__engine = create_engine('mysql://')

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

        Database.return_connection(self.connection)

