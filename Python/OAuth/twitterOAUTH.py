import urllib.parse as urlparse
import oauth2
from Configuration import twitterConstants
import Utilities.Logger_LocalDiskLogging as logger

# notify Twitter of our consumer who will try to login
consumer = oauth2.Consumer(twitterConstants.CONSUMER_KEY, twitterConstants.CONSUMER_SECRET)
access_token = oauth2.Token(twitterConstants.ACCESS_KEY, twitterConstants.ACCESS_SECRET)


def get_request_token():
    logger.logging_test.info('Consumer : {}'.format(consumer))
    # now establish ourself as the client who will make calls
    logger.logging_test.info('Consumer Key : {}'.format(consumer.key))
    client = oauth2.Client(consumer, access_token)
    # give us a token to make request for the consumer
    response, content = client.request(twitterConstants.REQUEST_TOKEN_URL, 'POST')
    # if something fails
    if response.status != 200:
        print("An error occurred getting the request token from Twitter")
        logger.logging_test.error("An error occurred getting the request token from Twitter")

    return dict(urlparse.parse_qsl(content.decode('utf-8')))

def get_oath_verifier(request_token):
    # test twitter links and token
    logger.logging_test.info('Oauth Verifier Requested For Request Token : {}'.format(request_token))
    print("Go to the following site in your browser:")
    print(get_oauth_verifier_url(request_token))

    logger.logging_test.info("User sent to the following URL : {}?oauth_token={}".format(
        twitterConstants.AUTHORIZATION_URL, request_token['oauth_token']))

    # need to get automatically for webAPI
    return input("What is the PIN from Twitter?")

def get_oauth_verifier_url(request_token):
    return "{}?oauth_token={}".format(twitterConstants.AUTHORIZATION_URL, request_token['oauth_token'])


def get_access_token(request_token, oath_verifier):
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oath_verifier)
    # repeat above but now with the valid request token
    client = oauth2.Client(consumer, token)
    # get access token now
    response, content = client.request(twitterConstants.ACCESS_TOKEN_URL, 'POST')

    return dict(urlparse.parse_qs(content.decode('utf-8')))
