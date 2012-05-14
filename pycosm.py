#!/usr/bin/env python
# encoding: utf-8
"""
pycosm.py

Created by John R. Southern (john.southern@softwerke.ca) on 2012-02-16.

Provide a means to interact with the Cosm (Pachube) API. The API provides a
RESTful interface which enables the following interactions:

GET : Retrieves the current state of the object
PUT : Sets the current state of the object
POST : Creates a new object
DELETE : Deletes the object

Refer to https://cosm.com/docs/ for detailed API documentation.

"""

import httplib
import unittest


class StreamIdError(Exception):
	def __init__(self, datastream_id):
		self.value = datastream_id
		
	def __str__(self):
		return repr(self.datastream_id)


class CosmDataStream(object):
	"""
	The CosmDataStream class provides a means through which to interact
	with the Cosm API. Although v2 of the API supports several different
	data formats (JSON, XML, CSV) for the response, currently only the default
	format (JSON) is supported here.
	"""
	def __init__(self, datastream_id=None, api_key=None):
		
		self.datastream_id = datastream_id
		self.api_key = api_key
		
	def get(self):
		"""
		Submit a GET request to the API, to get the current state of the stream.
		"""
		
		# before attempting to establish a connection to Cosm, make sure
		# that a stream_id has been specified
		if self.datastream_id is not None:
		
			# attempt to establish a connection to the Cosm API
			try:
			
				# submit the HTTP GET request to the API
				connection = httplib.HTTPConnection("api.cosm.com", 80)
				connection.request("GET", "/v2/feeds/%s" %self.datastream_id,
				 					headers = 	{
											  	"X-PachubeApiKey": self.api_key,
												"Accept": "application/json"
												})
		
				# get the resulting response
				response = connection.getresponse()
		
				# close the HTTP connection, now that we're finished with it
				# connection.close()
			
			# if, for some reason, we cannot communicate with the API (most
			# likely because of a network error), then allow the correspoding
			# exception to be raised
			except:
				raise
		
		# otherwise, raise an exception
		else:
			raise StreamIdError(self.datastream_id)
		
		return response

	def getDict(self):
		"""
		Submit a GET request, using the get() method, then convert the response
		into a Python dictionary object.
		"""
	
		# submit a GET request to retrieve the current state of the stream
		response = self.get()
		
		# convert the response into a dictionary
		state = eval(response.read())
		
		return state
		
		
	def put(self):
		"""
		Submit a PUT request to the API, to set the current state of the stream.
		"""
		
		pass
		

	def post(self):
		"""
		Submit a POST request to the API, to create a new stream.
		"""
		
		pass
		
		
	def delete(self):
		"""
		Submit a DELETE request to the API, to delete the current stream.
		"""
		
		pass
		


		
# Unit tests reside in this section...

class CosmDataStreamTests(unittest.TestCase):
	def setUp(self):
		pass

	def testAuthenticatedConnection(self):
		"""
		Instantiate a CosmDataStream object, with a unique stream ID and
		an API key.
		"""
		
		test_stream_id = "3194"
		test_api_key = "zwwPPs2NTKOJps8-UkSGHZdJLR6SAKw0TW1KcXk0QTJyUT0g"
		
		# establish a connection to the stream
		connection = CosmDataStream(test_stream_id, test_api_key)
		
		# submit a GET request to retrieve the current state of the stream
		response = connection.get()
		state = response.read()
		
		# we should receive a 200 status (200 OK: request processed successfully)
		self.assertEqual(response.status, 200)
		
	
	def testAnonymousConnection(self):
		"""
		Instantiate a CosmDataStream object, with a unique stream ID but
		without the required API key.
		"""
		
		test_stream_id = "3194"
		
		# establish a connection to the stream
		connection = CosmDataStream(test_stream_id)
		
		# submit a GET request to retrieve the current state of the stream
		response = connection.get()
		state = response.read()
		
		# we should receive a 401 status (401 Not Authorized)
		self.assertEqual(response.status, 401)

		
	def testEmptyConnection(self):
		"""
		Instantiate a CosmStream object, without a unique stream ID and
		without the required API key.
		"""
		
		# establish a connection to the stream
		connection = CosmDataStream()
		
		# an exception should be raised by the stream object upon attempting
		# to call the get() method without a stream_id having been specified
		self.assertRaises(StreamIdError, connection.get)


	def testGetDict(self):
		"""
		Attempt to call the getDict() method, which uses the get() method to
		get the current state of the stream, then returns the result as a
		Python dictionary object.
		"""

		test_stream_id = "3194"
		test_api_key = "zwwPPs2NTKOJps8-UkSGHZdJLR6SAKw0TW1KcXk0QTJyUT0g"
		
		# establish a connection to the stream
		connection = CosmDataStream(test_stream_id, test_api_key)
		
		# submit a GET request to retrieve the current state of the stream
		state = connection.getDict()
		#print('state: %s' %state)
		
		# the method should return a dictionary object
		self.assertEqual(type(state), dict)
		
		# attempt to access a few of the dictionary keys...
		
		# the 'feed' key in the dictionary should be
		# https://api.cosm.com/v2/feeds/3194.json
		self.assertEqual(state['feed'], 'https://api.cosm.com/v2/feeds/3194.json')
		
		# the 'id' key in the dictionary should be 3194
		self.assertEqual(state['id'], 3194)
		
		
if __name__ == '__main__':
	unittest.main()