# -*- coding: utf-8 -*-
import codecs
import json
import sys

import httplib2

#sys.stdout = codecs.getwriter('utf8')(sys.stdout)
#sys.stderr = codecs.getwriter('utf8')(sys.stderr)
import Utilities.Logger_LocalDiskLogging as logger

foursquare_client_id = "ASRWBUZJHURDV0TABWQFRCJA5TJL3TPSLDBIK22RTI5TJLCT"
foursquare_client_secret = "ULPEZYNSFCXT2XRTVWME2TORWVKQSJ1BEU12NQBPUR2X4BWH"
google_api_key = 'AIzaSyAW__6gKmgSq3iczkfQwIpmXayskyqqaf0'

def getGeocodeLocation(inputString):
    #Replace Spaces with '+' in URL
    locationString = inputString.replace(" ", "+")
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s'% (locationString, google_api_key))
    h = httplib2.Http()
    result = json.loads(h.request(url,'GET')[1])
    #print response
    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']
    logger.logging_test.info("Found coordinates : '{0}''{1}'".format(latitude, longitude))
    return (latitude,longitude)

#This function takes in a string representation of a location and cuisine type, geocodes the location, and then pass in the latitude and longitude coordinates to the Foursquare API
def findARestaurant(mealType, location):
    latitude, longitude = getGeocodeLocation(location)
    url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s,%s&query=%s' % (foursquare_client_id, foursquare_client_secret,latitude,longitude,mealType))
    h = httplib2.Http()
    result = json.loads(h.request(url,'GET')[1])
    if result['response']['venues']:
        #Grab the first restaurant
        restaurant = result['response']['venues'][0]
        venue_id = restaurant['id'] 
        restaurant_name = restaurant['name']
        restaurant_address = restaurant['location']['formattedAddress']
        #Format the Restaurant Address into one string
        address = ""
        for i in restaurant_address:
            address += i + " "
        restaurant_address = address
        
        #Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
        url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20150603&client_secret=%s' % ((venue_id,foursquare_client_id,foursquare_client_secret)))
        result = json.loads(h.request(url,'GET')[1])
        #Grab the first image
        #if no image available, insert default image url
        if result['response']['photos']['items']:
            firstpic = result['response']['photos']['items'][0]
            prefix = firstpic['prefix']
            suffix = firstpic['suffix']
            imageURL = prefix + "300x300" + suffix
        else:
            imageURL = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"

        restaurantInfo = {'name':restaurant_name, 'address':restaurant_address, 'image':imageURL}
        if str(type(restaurantInfo['name'])) != "<class 'bytes'>":
            logger.logging_test.info("Restaurant Name: {} ".format(restaurantInfo['name'].encode('utf-8')))
        else:
            logger.logging_test.info("Restaurant Name: Not printable ")
        if str(type(restaurantInfo['address'])) != "<class 'bytes'>":
            logger.logging_test.info("Restaurant Address: {} ".format(restaurantInfo['address'].encode('utf-8')))
        else:
            logger.logging_test.info("Restaurant Address: Not printable ")
            logger.logging_test.info("Image: %s \n " % restaurantInfo['image'])
        return restaurantInfo
    else:
        logger.logging_test.error("No Restaurants Found for %s" % location)
        logger.logging_test.error("No Restaurants Found")
        return "No Restaurants Found"
    
if __name__ == '__main__':
    logger.logging_test.info('Finding Pizza In Tokyo')
    findARestaurant("Pizza", "Tokyo, Japan")
    findARestaurant("Tacos", "Jakarta, Indonesia")
    findARestaurant("Tapas", "Maputo, Mozambique")
    findARestaurant("Falafel", "Cairo, Egypt")
    findARestaurant("Spaghetti", "New Delhi, India")
    findARestaurant("Cappuccino", "Geneva, Switzerland") 
    findARestaurant("Sushi", "Los Angeles, California")
    findARestaurant("Steak", "La Paz, Bolivia")
    findARestaurant("Gyros", "Sydney Austrailia")