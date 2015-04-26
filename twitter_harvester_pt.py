#!/usr/bin/env python
"""
Twitter harvester
Author: Luke Jones
Email: lukealexanderjones@gmail.com/lukej1@student.unimelb.edu.au
Student ID: 654645
Date: 25 April 2015
"""

import twitter
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

	#create api connection
	api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)

	#search for tweets within 100kms of brisbane city
	statuss = api.GetFollowers(screen_name='@magpiesaff')

	for status in statuss:
		print status.name

	#geocode= (-27.4709, 153.0235, '100km')

	# #print them for fun
	# for tweet in tweets:
	# 	print tweet



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