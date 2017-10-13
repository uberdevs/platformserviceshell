from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import Utilities.Logger_LocalDiskLogging as logger

Base = declarative_base()
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), index=True)
    first_name = Column(String(50), index=True)
    last_name = Column(String(50), index=True)
    oauth_token = oauth_token = Column(String(150), index=True)
    oauth_token_secret = Column(String(150), index=True)
    username = Column(String(32), index=True)
    password_hash = Column(String(64))


    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)
        logger.logging_database.info('Password Hash : {}'.format(self.password_hash) )

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in = expiration)
        logger.logging_database.info('Serializer : {}'.format(s.dumps({'id': self.id })))
        return s.dumps({'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            logger.logging_database.info('Token expired')
            #Valid Token, but expired
        # return None
        except BadSignature:
            logger.logging_database.info('Invalid Token')
            #Invalid Token
            return None
        user_id = data['id']
        return user_id

class Restaurant(Base):
  __tablename__ = 'restaurant'
  id = Column(Integer, primary_key=True)
  restaurant_name = Column(String)
  restaurant_address = Column(String)
  restaurant_image = Column(String)

  #Add a property decorator to serialize information from this database
  @property
  def serialize(self):
    return {
        'restaurant_name': self.restaurant_name,
        'restaurant_address': self.restaurant_address,
        'restaurant_image': self.restaurant_image,
        'id': self.id

    }

class Bagel(Base):
    __tablename__ = 'bagel'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    picture = Column(String)
    description = Column(String)
    price = Column(String)
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
	    'name' : self.name,
	    'picture' : self.picture,
	    'description' : self.description,
	    'price' : self.price
	        }
engine = create_engine('sqlite:///A:\\Work\\Python\\Vagrant\\api_server\\DB\\restaurants.db')
Base.metadata.create_all(engine)
