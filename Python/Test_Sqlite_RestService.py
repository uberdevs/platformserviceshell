import codecs
import json
import sys
import urllib.parse

from httplib2 import Http

import Utilities.Logger_LocalDiskLogging as logger

#sys.stdout = codecs.getwriter('utf8')(sys.stdout)
#sys.stderr = codecs.getwriter('utf8')(sys.stderr)

print("Running Endpoint Tester....\n")
address = input("Please enter the address of the server you want to access, \n If left blank the connection will be set to 'http://localhost:5000':   ")
if address == '':
	address = 'http://localhost:5000'



#TEST One -- READ ALL RESTAURANTS
try:
    logger.logging_test.info("Attempting Test 1: Reading all Restaurants...")
    h = Http()
    h.add_credentials('apiDefaultUser', 'P@$$W0rd')
    url = address + "/restaurants"
    data = dict(username = "apiDefaultUser", password = "P@$$W0rd")
    resp, content = h.request(url,'GET')#, urlencode(data))
    if resp['status'] != '200':
        logger.logging_test.error('Received an unsuccessful status code of %s' %
                    resp['status'])
        raise Exception('Received an unsuccessful status code of %s' %
                    resp['status'])
except Exception as err:
    logger.logging_test.error("Test 1 FAILED: Could not retrieve restaurants from server")
    print(err.args)
    sys.exit()
else:
    all_result = json.loads(content)
    print(content)
    logger.logging_test.info("Test 1 PASS: Succesfully read all restaurants")

    # Security TEST 2 TRY TO MAKE A NEW USER
    try:
        h = Http()
        url = address + '/users'
        logger.logging_test.info('URL : {}'.format(url))
        data = dict(username="apiDefaultUser", password="P@$$W0rd")
        data = json.dumps(data)
        logger.logging_test.info('Data : {}'.format(data))
        resp, content = h.request(url, 'POST', body=data, headers={
            "Content-Type": "application/json"})
        logger.logging_test.info('Response : {0} Content : {1}'.format(resp, content))
        if resp['status'] != '201' and resp['status'] != '200':
            logger.logging_test.error('Received an unsuccessful status code of %s' %
                                      resp['status'])
            raise Exception('Received an unsuccessful status code of %s' %
                            resp['status'])
    except Exception as err:
        logger.logging_test.error('Security Test 2 FAILED: Could not make a new user')
        print(err.args)
        sys.exit()
    else:
        logger.logging_test.error("Security Test 2 PASS: Succesfully made a new user")

    try:
        logger.logging_test.info("Main Test 1: Creating new Restaurant......")
        h = Http()
        h.add_credentials('apiDefaultUser', 'P@$$W0rd')
        url = address + '/restaurants?location=Buenos+Aires+Argentina&mealType=Sushi'
        data = dict(username="apiDefaultUser", password="P@$$W0rd")
        resp, result = h.request(url, 'POST', body=json.dumps(
            data), headers={"Content-Type": "application/json"})
        if resp['status'] != '200':
            logger.logging_test.error('Received an unsuccessful status code of %s' %
                                      resp['status'])
            raise Exception('Received an unsuccessful status code of %s' %
                            resp['status'])
        print(json.loads(result))

    except Exception as err:
        logger.logging_test.error("Test 2 FAILED: Could not add new restaurants")
        print(err.args)
        sys.exit()
    else:
        logger.logging_test.info("Test 2 PASS: Succesfully Made a new restaurants")

#TEST THREE -- READ A SPECIFIC RESTAURANT
    try:
        logger.logging_test.info("Attempting Test 3: Reading the last created restaurant...")
        result = all_result
        restID = 1
        url = address + "/restaurants/%s" % restID
        h = Http()
        h.add_credentials('apiDefaultUser', 'P@$$W0rd')
        resp, content = h.request(url,'GET')
        if resp['status'] != '200':
            logger.logging_test.error('Received an unsuccessful status code of %s' %
                               resp['status'])
            raise Exception('Received an unsuccessful status code of %s' %
                            resp['status'])
    except Exception as err:
        logger.logging_test.error("Test 3 FAILED: Could not retrieve restaurant from server")
        print(err.args)
        print(url)
        sys.exit()
    else:
        print(url)

        logger.logging_test.info("Test 3 PASS: Succesfully read last restaurant")

#TEST FOUR -- UPDATE A SPECIFIC RESTAURANT
    try:
        logger.logging_test.info("Attempting Test 4: Changing the name, image, and address of the first restaurant to ...")
        result = all_result
        restID = 1
        h = Http()
        h.add_credentials('apiDefaultUser', 'P@$$W0rd')
        url = address + "/restaurants/%s?name=Udacity&address=2465+Latham+Street+Mountain+View+CA&image=https://media.glassdoor.com/l/70/82/fc/e8/students-first.jpg" % restID
        print(url)
        data = dict(username = "apiDefaultUser", password = "P@$$W0rd")
        resp, content = h.request(url,'PUT', urllib.parse.urlencode(data))
        print(resp)
        if resp['status'] != '200':
            logger.logging_test.error('Received an unsuccessful status code of %s' %
                               resp['status'])
            raise Exception('Received an unsuccessful status code of %s' %
                            resp['status'])

    except Exception as err:
        logger.logging_test.error("Test 4 FAILED: Could not update restaurant from server")
        print(err.args)
        sys.exit()
    else:
        logger.logging_test.info("Test 4 PASS: Succesfully updated first restaurant")

#TEST FIVE -- DELETE SECOND RESTARUANT
try:
    logger.logging_test.info("Attempting Test 5: Deleteing the second restaurant from the server...")
    result = all_result
    restID = result['restaurants'][1]['id']
    h = Http()
    h.add_credentials('apiDefaultUser', 'P@$$W0rd')
    url = address + "/restaurants/%s" % restID
    print(url)
    data = dict(username = "apiDefaultUser", password = "P@$$W0rd")
    resp, content = h.request(url,'DELETE', urllib.parse.urlencode(data))
    print(resp)
    if resp['status'] != '200':
        logger.logging_test.error('Received an unsuccessful status code of %s' %
            resp['status'])
        raise Exception('Received an unsuccessful status code of %s' %
            resp['status'])
except Exception as err:
    logger.logging_test.error("Test 5 FAILED: Could not delete restaurant from server")
    print(err.args)
    sys.exit()
else:
    logger.logging_test.info("Test 5 PASS: Succesfully updated first restaurant")
    logger.logging_test.info("ALL TESTS PASSED!")
