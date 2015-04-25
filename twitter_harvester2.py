#!/usr/bin/env python
"""
Twitter harvester
Author: Luke Jones
Email: lukealexanderjones@gmail.com/lukej1@student.unimelb.edu.au
Student ID: 654645
Date: 25 April 2015
"""

import tweepy
import couchdb
import csv
import json
from pprint import pprint as pp

"""
Note: I have stored my keys locally in a space delminated text file as I don't want to share on GitHub.
Just store the keys in the format;
consumer_key consumer_secret access_token_key access_token_secret
and point the keyfile to it and everything should work fine.

Alternatively just drop them into the relevant fields.
"""

keyfile = '/Users/lukejones/Developer/twitter_harvester/auth.txt' #change to command line arg later

def main():

	#set the keys
	consumer_key, consumer_secret, access_token_key, access_token_secret = set_keys(keyfile)

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token_key, access_token_secret)

	api = tweepy.API(auth)
	places = api.geo_search(query='Brisbane', granularity="city")
	place_id = places[0].id

	tweets = api.search(q="place:%s" % place_id)
	for tweet in tweets:
	    print tweet.text + " | " + tweet.place.name if tweet.place else "Undefined place"


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