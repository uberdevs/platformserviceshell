import json

import httplib2
import requests



from flask import Flask, jsonify, request, abort, g
from flask import make_response
from flask import render_template
from flask_httpauth import HTTPBasicAuth
from oauth2client.client import FlowExchangeError
from oauth2client.client import flow_from_clientsecrets
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
sys.path.append("..")
import Utilities.Logger_LocalDiskLogging as logger
from DB.Models_Sqlite import Base, Restaurant, Bagel, User
from Test_Google_GEOCode import findARestaurant

app = Flask(__name__)
auth = HTTPBasicAuth()

#sys.stdout = codecs.getwriter('utf8')(sys.stdout)
#sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "GETYOUROWN"
foursquare_client_secret = "GETYOUROWN"
google_api_key = 'GETYOUROWN'

engine = create_engine('sqlite:///A:\\Work\\Python\\Vagrant\\api_server\\DB\\restaurants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


CLIENT_ID = json.loads(
    open('.//Configuration//google_client_secrets.json', 'r').read())['web']['client_id']


@auth.verify_password
def verify_password(username_or_token, password):
    logger.logging_rest_service.info('Got user to test : {} ', username_or_token)
    #Try to see if it's a token first
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(id = user_id).one()
        logger.logging_rest_service.info('User ID Found For : {}',username_or_token)
    else:
        user = session.query(User).filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            logger.logging_rest_service.error('Username or password is not correct : {}', username_or_token)
            return False
    g.user = user
    return True

@app.route('/clientOAuth')
def start():
    return render_template('googleClientOAUTH.html')

@app.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    logger.logging_rest_service.info('Auth Token Received : {} ', token )
    return jsonify({'token': token.decode('ascii')})

@app.route('/oauth/<provider>', methods = ['POST'])
def login(provider):
    #STEP 1 - Parse the auth code
    auth_code = request.json.get('auth_code')
    logger.logging_rest_service.info('Auth Code Received : {} ', auth_code )
    print("Step 1 - Complete, received auth code %s" % auth_code)
    logger.logging_rest_service.info("Step 1 - Complete")
    if provider == 'google':
        #STEP 2 - Exchange for a token
        try:
            # Upgrade the authorization code into a credentials object
            oauth_flow = flow_from_clientsecrets('google_client_secrets.json', scope='')
            oauth_flow.redirect_uri = 'postmessage'
            credentials = oauth_flow.step2_exchange(auth_code)
        except FlowExchangeError:
            response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
            response.headers['Content-Type'] = 'application/json'
            logger.logging_rest_service.error('Error encountered : {} ', response)
            return response

        # Check that the access token is valid.
        access_token = credentials.access_token
        url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
        h = httplib2.Http()
        result = json.loads(h.request(url, 'GET')[1])
        # If there was an error in the access token info, abort.
        if result.get('error') is not None:
            response = make_response(json.dumps(result.get('error')), 500)
            response.headers['Content-Type'] = 'application/json'
            logger.logging_rest_service.error('Error Received Back : {} ', response)

        # # Verify that the access token is used for the intended user.
        # gplus_id = credentials.id_token['sub']
        # if result['user_id'] != gplus_id:
        #     response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
        #     response.headers['Content-Type'] = 'application/json'
        #     return response

        # # Verify that the access token is valid for this app.
        # if result['issued_to'] != CLIENT_ID:
        #     response = make_response(json.dumps("Token's client ID does not match app's."), 401)
        #     response.headers['Content-Type'] = 'application/json'
        #     return response

        # stored_credentials = login_session.get('credentials')
        # stored_gplus_id = login_session.get('gplus_id')
        # if stored_credentials is not None and gplus_id == stored_gplus_id:
        #     response = make_response(json.dumps('Current user is already connected.'), 200)
        #     response.headers['Content-Type'] = 'application/json'
        #     return response
        print("Step 2 Complete! Access Token : %s " % credentials.access_token)
        logger.logging_rest_service.info("Step 2 Complete! ")

        #STEP 3 - Find User or make a new one

        #Get user info
        h = httplib2.Http()
        userinfo_url =  "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': credentials.access_token, 'alt':'json'}
        answer = requests.get(userinfo_url, params=params)

        data = answer.json()

        name = data['name']
        picture = data['picture']
        email = data['email']

        #see if user exists, if it doesn't make a new one
        user = session.query(User).filter_by(email=email).first()
        if not user:
            logger.logging_rest_service.info("User not found.  Making a new one. : {} ", name)
            user = User(username = name, picture = picture, email = email)
            session.add(user)
            session.commit()


        #STEP 4 - Make token
        token = user.generate_auth_token(600)
        logger.logging_rest_service.info('Got token : {} ', token)

        #STEP 5 - Send back token to the client
        return jsonify({'token': token.decode('ascii')})

        ## uncomment to make the token expire in 10 minutes or 600 seconds
        #return jsonify({'token': token.decode('ascii'), 'duration': 600})
    else:
        logger.logging_rest_service.error('Unrecognized Provider')
        return 'Unrecognized Provider'

@app.route('/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        logger.logging_rest_service.error('Missing an argument(s)')
        print("missing arguments")
        abort(400)

    if session.query(User).filter_by(username = username).first() is not None:
        print("existing user")
        logger.logging_rest_service.info('Existing User')
        user = session.query(User).filter_by(username=username).first()
        return jsonify({'message':'user already exists'}), 200#, {'Location': url_for('get_user', id = user.id, _external = True)}

    user = User(username = username)
    user.hash_password(password)
    session.add(user)
    session.commit()
    logger.logging_rest_service.info('User : {} ', jsonify({ 'username': user.username }))
    return jsonify({ 'username': user.username }), 201#, {'Location': url_for('get_user', id = user.id, _external = True)}

@app.route('/users/<int:id>')
def get_user(id):
    user = session.query(User).filter_by(id=id).one()
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@app.route('/resource')
@auth.login_required
def get_resource():
    return jsonify({ 'data': 'Hello, %s!' % g.user.username })


@app.route('/restaurants', methods=['GET', 'POST'])
@auth.login_required
def all_restaurants_handler():
  if request.method == 'GET':
    # RETURN ALL RESTAURANTS IN DATABASE
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants=[i.serialize for i in restaurants])

  elif request.method == 'POST':
    # MAKE A NEW RESTAURANT AND STORE IT IN DATABASE
    location = request.args.get('location', '')
    mealType = request.args.get('mealType', '')
    restaurant_info = findARestaurant(mealType, location)
    if restaurant_info != "No Restaurants Found":
      restaurant = Restaurant(restaurant_name= restaurant_info['name'], restaurant_address=
          restaurant_info['address'], restaurant_image=restaurant_info['image'])
      session.add(restaurant)
      session.commit()
      logger.logging_rest_service.info('Restaurant Found : {} ', jsonify(restaurant=restaurant.serialize))
      return jsonify(restaurant=restaurant.serialize)
    else:
        logger.logging_rest_service.error("error : No Restaurants Found for %s in %s" % (mealType, location))
    return jsonify({"error": "No Restaurants Found for %s in %s" % (mealType, location)})


@app.route('/restaurants/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def restaurant_handler(id):
  restaurant = session.query(Restaurant).filter_by(id=id).one()
  if request.method == 'GET':
      #RETURN A SPECIFIC RESTAURANT
      logger.logging_rest_service.info('Restaurant Found : {} ', jsonify(restaurant=restaurant.serialize))
      return jsonify(restaurant=restaurant.serialize)
  elif request.method == 'PUT':
      #UPDATE A SPECIFIC RESTAURANT
      address = request.args.get('address')
      image = request.args.get('image')
      name = request.args.get('name')
      if address:
          restaurant.restaurant_address = address
      if image:
          restaurant.restaurant_image = image
      if name:
          restaurant.restaurant_name = name

      session.commit()
      return jsonify(restaurant=restaurant.serialize)

  elif request.method == 'DELETE':
      #DELETE A SPECFIC RESTAURANT
      session.delete(restaurant)
      session.commit()
  logger.logging_rest_service.info('Restaurant deleted')
  return "Restaurant Deleted"

@app.route('/bagels', methods = ['GET','POST'])
@auth.login_required
def showAllBagels():
    if request.method == 'GET':
        bagels = session.query(Bagel).all()
        logger.logging_rest_service.info('Bagel Found : {} ', jsonify(bagels = [bagel.serialize for bagel in bagels]))
        return jsonify(bagels = [bagel.serialize for bagel in bagels])
    elif request.method == 'POST':
        name = request.json.get('name')
        description = request.json.get('description')
        picture = request.json.get('picture')
        price = request.json.get('price')
        newBagel = Bagel(name = name, description = description, picture = picture, price = price)
        session.add(newBagel)
        session.commit()
        logger.logging_rest_service.info('Bagel Found : {} ', jsonify(newBagel.serialize))
        return jsonify(newBagel.serialize)


if __name__ == '__main__':
    app.debug = True
    logger.logging_rest_service.info('Starting listener')
    app.run(host='0.0.0.0', port=5000)
