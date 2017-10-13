import requests
from flask import Flask, render_template, session, redirect, request, url_for, g

import sys
sys.path.append("..")
from DB.DatabaseConnection_postgreSQL import Database
from DB.Models_Postgresql import User
from OAuth.twitterOAUTH import get_request_token, get_oauth_verifier_url, get_access_token
import Utilities.Logger_LocalDiskLogging as logger


app = Flask(__name__)
app.secret_key = 'P@$$W0rd'

Database.initialise(host='localhost', database='restful_api', user='apiDefaultUser', password='P@$$W0rd')


@app.before_request
def load_user():
    if 'screen_name' in session:
        g.user = User.load_from_db_by_screen_name(session['screen_name'])
        logger.logging_rest_service.info('Found user : {}', g.user.username)


@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/login/twitter')
def twitter_login():
    if 'screen_name' in session:
        return redirect(url_for('profile'))
    request_token = get_request_token()
    logger.logging_rest_service.info('Request Token Received : {}', request_token)
    session['request_token'] = request_token

    return redirect(get_oauth_verifier_url(request_token))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('homepage'))


@app.route('/auth/twitter')  # http://127.0.0.1:4995/auth/twitter?oauth_verifier=1234567
def twitter_auth():
    oauth_verifier = request.args.get('oauth_verifier')
    access_token = get_access_token(session['request_token'], oauth_verifier)
    logger.logging_rest_service.info('Access Token Received : {}', access_token)
    user = User.load_from_db_by_screen_name(access_token['screen_name'])
    if not user:
        user = User(access_token['screen_name'], access_token['oauth_token'],
                    access_token['oauth_token_secret'], None)
        user.save_to_db()
        logger.logging_rest_service.info('New User Saved To DB')

    session['screen_name'] = user.screen_name

    return redirect(url_for('profile'))


@app.route('/profile')
def profile():
    return render_template('profile.html', user=g.user)


@app.route('/search')
def search():
    query = request.args.get('q')
    tweets = g.user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q={}'.format(query))

    tweet_texts = [{'tweet': tweet['text'], 'label': 'neutral'} for tweet in tweets['statuses']]
    logger.logging_rest_service.info('Tweet Text Pulled : {}', tweet_texts)

    for tweet in tweet_texts:
        r = requests.post('http://text-processing.com/api/sentiment/', data={'text': tweet['tweet']})
        json_response = r.json()
        label = json_response['label']
        tweet['label'] = label

    return render_template('search.html', content=tweet_texts)

if __name__ == '__main__':
    app.debug = True
    logger.logging_rest_service.info('Starting listener')
    app.run(host='0.0.0.0', port=5000)