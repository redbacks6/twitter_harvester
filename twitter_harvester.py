#!/usr/bin/env python
"""
Twitter harvester
Author: Luke Jones
Email: lukealexanderjones@gmail.com/lukej1@student.unimelb.edu.au
Student ID: 654645
Date: 30 April 2015
"""

import tweepy
import couchdb
import csv
import json
import sys
from pprint import pprint as pp

"""
Note: I have stored my keys locally in a space delminated text file as I don't want to share on GitHub.
Just store the keys in the format;
consumer_key consumer_secret access_token_key access_token_secret
and point the keyfile to it and everything should work fine.

Alternatively just drop them into the relevant fields.
"""

##TODO change to command line argument - easier here for now
keyfile = sys.argv[1] #'/Users/lukejones/Developer/twitter_harvester/auth.txt'
couchlogin = sys.argv[2] #'/Users/lukejones/Developer/twitter_harvester/couchDB.txt'
couchserver = sys.argv[3] #'http://115.146.95.216:5984/'
database = sys.argv[4] #'brisbanetweets'
location = [float(x) for x in sys.argv[5].split(',')] #[153.81,-27.75,153.24,-27.11]

def main():

	#setup database connection https://pythonhosted.org/CouchDB/getting-started.html
	couch = couchdb.Server(couchserver)
	username, password = get_login(couchlogin)
	couch.resource.credentials = (username, password)

	#check if database created if Exception create it
	try:
		db = couch[database]
	except Exception, e:
		db = couch.create(database)

	#set the keys
	consumer_key, consumer_secret, access_token_key, access_token_secret = set_keys(keyfile)

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token_key, access_token_secret)

	# If using the REST API then use this constructor
	api = tweepy.API(auth)

	# Constructor for streaming API
	sapi = tweepy.streaming.Stream(auth=auth, listener=CustomStreamListener(api, db))    
	sapi.filter(locations=location)


#override the base listener
class CustomStreamListener(tweepy.StreamListener):
	
	def __init__(self, api, db):
		self.db = db
		self.api = api
		super(tweepy.StreamListener, self).__init__()

	def on_status(self, status):
		
		#Add to database
		self.db.save(status._json)
		
	def on_error(self, status_code):
		print >> sys.stderr, 'Encountered error with status code:', status_code
		return True # Don't kill the stream

	def on_timeout(self):
		print >> sys.stderr, 'Timeout...'
		return True # Don't kill the stream


#Helper method to set the keys
def set_keys(keyfile):
	with open(keyfile) as textfile:
		keys = textfile.readline().split()

		consumer_key = keys[0]
		consumer_secret = keys[1]
		access_token_key = keys[2]
		access_token_secret = keys[3]

	return consumer_key, consumer_secret, access_token_key, access_token_secret

#Helper method to set the keys
def get_login(loginfile):
	with open(loginfile) as textfile:
		logins = textfile.readline().split()

		username = logins[0]
		password = logins[1]

	return username, password

# Run the Main Method
if __name__ == '__main__':
    main()