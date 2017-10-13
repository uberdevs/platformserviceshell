from DB.Models_Postgresql import User
from DB.DatabaseConnection_postgreSQL import Database
from OAuth.twitterOAUTH import get_request_token, get_oath_verifier, get_access_token
import Utilities.Logger_LocalDiskLogging as logger

Database.initialise(user='apiDefaultUser', password='P@$$W0rd', host='localhost', database='restful_api')

user_email = input("Enter your e-mail address: ")
logger.logging_test.info('User Email : {}'.format(user_email))

user = User.load_from_db_by_email(user_email)

if not user:
    logger.logging_test.info('No user found.  Requesting data')
    request_token = get_request_token()
    logger.logging_test.info('Token received : {0}'.format(request_token))
    oauth_verifier = get_oath_verifier(request_token)
    logger.logging_test.info('OAuth Verifier Received : {0}'.format(oauth_verifier))
    access_token = get_access_token(request_token, oauth_verifier)
    logger.logging_test.info('Access Token Received : {0}'.format(access_token))
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    logger.logging_test.info('Name Given : {0} {1}'.format(first_name, last_name))

    user = User(user_email, first_name, last_name, access_token['oauth_token'], access_token['oauth_token_secret'], None)
    user.save_to_db()


tweets = user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images')

for tweet in tweets['statuses']:
    print(tweet['text'])