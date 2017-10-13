#THIS IS A WEBSERVER FOR DEMONSTRATING THE TYPES OF RESPONSES WE SEE FROM AN API ENDPOINT
from flask import Flask

import sys
sys.path.append("..")
import Utilities.Logger_LocalDiskLogging as logger

api_Rest_Service = Flask(__name__)

#GET REQUEST

@api_Rest_Service.route('/readHello')
def getRequestHello():
	logger.logging_rest_service.info('Route /readHello called')
	return "Hi, I got your GET Request!"

#POST REQUEST
@api_Rest_Service.route('/createHello', methods = ['POST'])
def postRequestHello():
	logger.logging_rest_service.info('Route /createHello called')
	return "I see you sent a POST message :-)"
	
#UPDATE REQUEST
@api_Rest_Service.route('/updateHello', methods = ['PUT'])
def updateRequestHello():
	logger.logging_rest_service.info('Route /updateHello called')
	return "Sending Hello on an PUT request!"

#DELETE REQUEST
@api_Rest_Service.route('/deleteHello', methods = ['DELETE'])
def deleteRequestHello():
	logger.logging_rest_service.info('Route /deleteHello called')
	return "Deleting your hard drive.....haha just kidding! I received a DELETE request!"

if __name__ == '__main__':
	api_Rest_Service.debug = True
	logger.logging_rest_service.info('Starting listener')
	api_Rest_Service.run(host='0.0.0.0', port=5000)