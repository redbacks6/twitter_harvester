#!/usr/bin/env python
"""
Twitter duplicate eliminator
Author: Luke Jones
Email: lukealexanderjones@gmail.com/lukej1@student.unimelb.edu.au
Student ID: 654645
Date: 5 May 2015
"""

import tweepy
import couchdb
import csv
import json
import sys
from pprint import pprint as pp

##Command line args
couchlogin = '/Users/lukejones/Developer/twitter_harvester/couchDB.txt'
couchserver = 'http://115.146.95.161:5984/'
database_dirty = 'brisbanetweets'
database_clean = 'brisbane_cleaned'

def main():

	#setup database connection https://pythonhosted.org/CouchDB/getting-started.html
	couch = couchdb.Server(couchserver)
	username, password = get_login(couchlogin)
	couch.resource.credentials = (username, password)

	#check if database created if Exception create it
	try:
		dirty_db = couch[database_dirty]
		clean_db = couch[database_clean]
	except Exception, e:
		print 'No database with that name!'
	
	#set some counters
	count1 = 1 #processed docs
	count2 = 0 #docs added new DB

	for doc in dirty_db:

		tweet = dirty_db[doc]

		tweet['_id'] = tweet['id_str']

		if tweet['_id'] not in clean_db:
		 	clean_db.save(tweet)
		 	count2 += 1

		if (count1 % 100) == 0:
			print 'Processed %s documents' %(count1)
		count1 += 1

	print 'Added %s documents to the %s database' %(count2, database_clean)

			
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