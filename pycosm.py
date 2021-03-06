#!/usr/bin/env python
# encoding: utf-8
"""
pycosm.py

Created by John R. Southern (https://github.com/gogojohn) on 2012-02-16.

Provide a means to interact with the Cosm (Pachube) API. The API provides a
RESTful interface which enables the following interactions:

GET : Retrieves the current state of the object
PUT : Sets the current state of the object
POST : Creates a new object
DELETE : Deletes the object

Refer to https://cosm.com/docs/ for detailed API documentation.

"""

import httplib
import json
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
	def __init__(self, feed_id=None, datastream_id=None, api_key=None):
		
		self.feed_id = feed_id
		self.datastream_id = datastream_id
		self.api_key = api_key

	def get(self):
		"""
		Submit a GET request to the API, to get the current state of the
		stream.
		"""

		# before attempting to establish a connection to Cosm, make sure
		# that a feed_id has been specified
		if self.feed_id is not None:

			# attempt to establish a connection to the Cosm API
			try:

				# submit the HTTP GET request to the API
				connection = httplib.HTTPSConnection("api.cosm.com", 443)
				connection.request("GET", "/v2/feeds/%s/datastreams/%s"
				 					%(self.feed_id, self.datastream_id),
				 					headers = 	{
											  	"X-ApiKey": self.api_key,
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
		state = json.loads(response.read())
		
		return state


	def put(self, body_content):
		"""
		Submit a PUT request to the API, to set the current state of the stream.
		"""

		# before attempting to establish a connection to Cosm, make sure
		# that a feed_id and stream_id have been specified
		if self.feed_id is not None and self.datastream_id is not None:

			# attempt to establish a connection to the Cosm API
			try:

				connection = httplib.HTTPSConnection("api.cosm.com", 443)
				connection.request("PUT", "/v2/feeds/%s/datastreams/%s"
				 					%(self.feed_id, self.datastream_id),
							body_content,
							headers = 	{
									  	"X-ApiKey": self.api_key,
										"Accept": "application/json"
										}
							)

				# get the resulting response
				response = connection.getresponse()

			# if, for some reason, we cannot communicate with the API (most
			# likely because of a network error), then allow the correspoding
			# exception to be raised
			except:
				raise

		# otherwise, raise an exception
		else:
			raise StreamIdError(self.datastream_id)

		return response


	def post(self, body_content):
		"""
		Submit a POST request to the API, to create a new datastream,
		or datapoint.
		"""

		# before attempting to establish a connection to Cosm, make sure
		# that a feed_id has been specified
		if self.feed_id is not None:

			# attempt to establish a connection to the Cosm API
			try:

				# submit the HTTP POST request to the API
				connection = httplib.HTTPSConnection("api.cosm.com", 443)
				connection.request(	"POST",
				 					"/v2/feeds/%s/datastreams/%s/datapoints"
				 					%(self.feed_id, self.datastream_id),
									body_content,
				 					headers = 	{
											  	"X-ApiKey": self.api_key,
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
		
		
	def postDatapointsDict(self, datapoints):
		"""
		Create new datapoints, for this datastream, using the provided
		dictionary. The key:value pairs in the dictionary must be in the
		following form:
		
			ISO 8601 formatted date-timestamp : value
			
		This dictionary is then converted to a JSON string, in the required
		format, so that the datastream can be updated to include the provided
		datapoints.
		"""
		
		# create an empty dictionary of datapoints for the JSON string
		datapointsDict = {"datapoints":[]}
		
		# next, iterate through the dictionary keys
		for key in datapoints.keys():
		
			# append each date-timestampt:value pair
			datapointsDict["datapoints"].append({
												"at":key,
												"value":datapoints[key]
												})
		
		# build the JSON formatted body content for the request
		body_content = json.dumps(datapointsDict)
		
		# and, finally, submit the POST request, to update the datastream
		response = self.post(body_content)
		
		return response
		
		
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

		test_feed_id = "59484"
		test_stream_id = "unittest"
		test_api_key = "RJcgiqm-gL7t8IVi42G-4kkjhlCSAKxRUHVGdSszWEZPMD0g"

		# establish a connection to the stream
		connection = CosmDataStream(test_feed_id, test_stream_id, test_api_key)

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

		test_feed_id = "59484"
		test_stream_id = "unittest"
		test_api_key = "RJcgiqm-gL7t8IVi42G-4kkjhlCSAKxRUHVGdSszWEZPMD0g"

		# establish a connection to the stream
		connection = CosmDataStream(test_feed_id, test_stream_id, test_api_key)
		
		# submit a GET request to retrieve the current state of the stream
		state = connection.getDict()
		# print('state: %s' %state)

		# the method should return a dictionary object
		self.assertEqual(type(state), dict)
		
		# attempt to access a few of the dictionary keys...

		# the 'id' key in the dictionary should be 'unittest'
		self.assertEqual(state['id'], 'unittest')


	def testPut(self):
		"""
		Attempt to set the current state of the stream, using the put() method.
		"""

		# this key and stream are for unit testing only, feel free to
		# substitute them with one of your own (but the key must have
		# read and update permission for the stream)
		test_feed_id = "59484"
		test_stream_id = "unittest"
		test_api_key = "RJcgiqm-gL7t8IVi42G-4kkjhlCSAKxRUHVGdSszWEZPMD0g"

		# establish a connection to the stream
		connection = CosmDataStream(test_feed_id, test_stream_id, test_api_key)

		# submit a PUT request to update the current state of the stream
		state = """{"current_value":"42"}"""
		response = connection.put(state)

		# we should receive a 200 status (200 OK: request processed successfully)
		self.assertEqual(response.status, 200)


	def testPostDatapointsDict(self):
		"""
		Attempt to create historical datapoints in the stream, using the
		postDatapointsDict() method.
		"""

		# this key and stream are for unit testing only, feel free to
		# substitute them with one of your own (but the key must have
		# create, read and update permission for the stream)
		test_feed_id = "59484"
		test_stream_id = "unittest"
		test_api_key = "RJcgiqm-gL7t8IVi42G-4kkjhlCSAKxRUHVGdSszWEZPMD0g"

		# establish a connection to the stream
		connection = CosmDataStream(test_feed_id, test_stream_id, test_api_key)
	
		# create a dictionary of datapoints
		datapoints = 	{
						"2013-01-14T12:00:00Z":"30",
						"2013-01-14T12:05:00Z":"35",
						"2013-01-14T12:10:00Z":"40",
						"2013-01-14T12:15:00Z":"35",
						"2013-01-14T12:20:00Z":"30",
						}

		response = connection.postDatapointsDict(datapoints)
		
		# we should receive a 200 status (200 OK: request processed successfully)
		self.assertEqual(response.status, 200)
		
		


if __name__ == '__main__':
	unittest.main()