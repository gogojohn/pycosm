#!/usr/bin/env python
# encoding: utf-8
"""
cosm-feed.py

Created by John R. Southern (john.southern@softwerke.ca) on 2012-02-16.

Query the Cosm (Pachube) API, using the provided datastream ID and API key. The
output is the raw data (JSON, by default) returned by the query.

"""

import sys
import getopt

import pycosm


help_message = '''
Query the Cosm API for the current state of the specified feed.

Usage: cosm-feed.py [options]
Options:
  -s <datastream ID>		The datastream ID to query the state of.
  --streamid=<datastream ID>	Same as -s.	
  -k <api key>			The Cosm API key to use when accessing the service.
  --apikey=<API key>		Same as -k.
'''


class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg


def main(argv=None):
	if argv is None:
		argv = sys.argv
	try:
		try:
			datastream_id = None
			api_key = None
			opts, args = getopt.getopt(argv[1:], "ho:vs:k:", ["help", "output=", "datastream_id=", "api_key="])
			
		except getopt.error, msg:
			raise Usage(msg)
	
		# option processing
		for option, value in opts:
			if option == "-v":
				verbose = True
			if option in ("-h", "--help"):
				raise Usage(help_message)
			if option in ("-o", "--output"):
				output = value
			if option in ("-s", "--streamid"):
				datastream_id = value
			if option in ("-k", "--apikey"):
				api_key = value
	
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "\t for help use --help"
		return 2


	# provided that we have a stream ID and an API key, then we're
	# ready to attempt to query the API
	if datastream_id is not None and api_key is not None:
		# establish a connection to the stream
		connection = cosm.CosmDataStream(datastream_id, api_key)

		# submit a GET request to retrieve the current state of the stream
#		response = connection.get()
#		state = response.read()

		state = connection.getDict()

		# display the response
		print("\ndatastream ID: %s\nAPI key: %s\nstate: %s\n" %(datastream_id, api_key, state))
	
	# otherwise, inform the user that we're missing something important	
	else:
		print("Error: a stream ID and API key must be specified")



if __name__ == "__main__":
	sys.exit(main())
