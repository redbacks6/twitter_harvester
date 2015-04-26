#!/usr/bin/env python
"""
Twitter harvester
Author: Luke Jones
Email: lukealexanderjones@gmail.com/lukej1@student.unimelb.edu.au
Student ID: 654645
Date: 26 April 2015
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
keyfile = '/Users/lukejones/Developer/twitter_harvester/auth.txt'

def main():

	#set the keys
	consumer_key, consumer_secret, access_token_key, access_token_secret = set_keys(keyfile)

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token_key, access_token_secret)

	# If using the REST API then use this constructor
	# api = tweepy.API(auth)

	# Constructor for streaming API
	sapi = tweepy.streaming.Stream(auth=auth, listener=CustomStreamListener())    
	sapi.filter(locations=[153.02,-27.47,153.12,-27.26])


class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        
        #DO SOMETHING WITH THE TWEETS HERE!
        #Print the json object to the screen for now...
        print pp(status._json)

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

# Run the Main Method
if __name__ == '__main__':
    main()