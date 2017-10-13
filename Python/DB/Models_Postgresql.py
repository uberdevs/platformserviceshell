import json

import oauth2

from DB.DatabaseConnection_postgreSQL import CursorFromConnectionFromPool
from OAuth.twitterOAUTH import consumer
from Utilities.Logger_LocalDiskLogging import logging


class User:
    def __init__(self, email, first_name, last_name, oauth_token, oauth_token_secret, username, password_hash, id):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.oauth_token = oauth_token
        self.oauth_token_secret
        self.username = username
        self.password_hash = password_hash
        self.id = id

    def __repr__(self):
        return "User {}".format(self.email)

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO user (email, first_name, last_name,auth_token, auth_token_secret, username, password_hash)'
                           ' VALUES(%s,%s,%s,%s,%s,%s,%s)',
                           (self.email,
                            self.first_name,
                            self.last_name,
                            self.oauth_token,
                            self.oauth_token_secret,
                            self.username,
                            self.password_hash))


    @classmethod
    def load_from_db_by_email(cls, email):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            user_data = cursor.fetchone()
            if user_data:
                return cls(email=user_data[1],
                           first_name=user_data[2],
                           last_name=user_data[3],
                           oauth_token=user_data[4],
                           oauth_token_secret=user_data[5],
                           username = user_data[6],
                           password_hash=user_data[7],
                           id=user_data[0])


    def twitter_request(self, uri, verb='GET'):
        # create an 'authorized_token' Token object and use that to perform Twitter API callas on behalf of the user or login to application
        authorized_token = oauth2.Token(self.oauth_token, oauth2.oath_token_secret)
        authorized_client = oauth2.Client(consumer, authorized_token)

        # make Twitter API Calls to test
        response, content = authorized_client.request(uri, verb)
        if response.status != 200:
            logging.error('An error occurred when searching tweets!')


        return json.loads(content.encode('utf-8'))

    @classmethod
    def load_from_db_by_screen_name(cls, screen_name):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM users WHERE screen_name=%s', (screen_name,))
            user_data = cursor.fetchone()
            if user_data:
                return cls(screen_name=user_data[1], oauth_token=user_data[2],
                           oauth_token_secret=user_data[3], id=user_data[0])