import hashlib
import oauth2 as oauth
import time
import urllib
import json
import urllib.parse
from Configuration import facebookConstants
import Utilities.Logger_LocalDiskLogging as logger
from django.http import HttpResponseRedirect
import requests


def connect_fb_social(request):
    """ This the main connecting function for fb """
    callback_url = 'http://' + request.META['HTTP_HOST'] + '/connect/facebook/complete/'
    return HttpResponseRedirect(facebookConstants.FACEBOOK_REQUEST_TOKEN_URL + '?client_id=%s&redirect_uri=%s&scope=%s'
                                % (facebookConstants.FACEBOOK_APP_ID, urllib.parse.quote(callback_url), 'email'))


def web_connect_facebook(request):
    """ Gets the access token and profile info from facebook """
    code = request.GET.get('code')
    consumer = oauth.Consumer(key=facebookConstants.FACEBOOK_APP_ID, secret=facebookConstants.FACEBOOK_APP_SECRET)
    client = oauth.Client(consumer)
    redirect_uri = 'http://' + request.META['HTTP_HOST'] + '/connect/facebook/complete/'
    request_url = facebookConstants.FACEBOOK_ACCESS_TOKEN_URL + '?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s' % (
        facebookConstants.FACEBOOK_APP_ID, redirect_uri, facebookConstants.FACEBOOK_APP_SECRET, code)
    resp, content = client.request(request_url, 'GET')
    access_token = dict(urllib.parse.parse_qsl(content))['access_token']
    request_url = facebookConstants.FACEBOOK_CHECK_AUTH + '?access_token=%s' % access_token

    if resp['status'] == '200':
        resp, content = client.request(request_url, 'GET')
        content_dict = json.loads(content)
        userid = content_dict['id']
    else:
        userid = None

    return userid

def get_fb_app_token():
    payload = {'grant_type': 'client_credentials', 'client_id': facebookConstants.FACEBOOK_APP_ID, 'client_secret': facebookConstants.FACEBOOK_APP_SECRET}
    file = requests.post('https://graph.facebook.com/oauth/access_token?', params = payload)
    result = file.text.split("=")[1]
    return result