#!/usr/bin/env python
"""
Twitter harvester - crawler
Author: Luke Jones
Email: lukealexanderjones@gmail.com/lukej1@student.unimelb.edu.au
Student ID: 654645
Date: 10 May 2015
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

##Command line args
keyfile = sys.argv[1] #'/Users/lukejones/Developer/twitter_harvester/auth.txt' #- space delinated keys
couchlogin = sys.argv[2] #'/Users/lukejones/Developer/twitter_harvester/couchDB.txt' #- space delineated login
couchserver = sys.argv[3] #'http://115.146.95.161:5984/'
database_ref = sys.argv[4] #'brisbane_cleaned'
# database_tl = sys.argv[5] #'brisbane_timeline_test1' #Only using one database
location = sys.argv[5] #'Brisbane, Queensland'


def main():

	"""
	Set up the couchDB connections
	"""
	#setup database connection https://pythonhosted.org/CouchDB/getting-started.html
	couch = couchdb.Server(couchserver)
	username, password = get_login(couchlogin)
	couch.resource.credentials = (username, password)

	#Connect to the database to find users
	try:
		db_users = couch[database_ref]
	except Exception, e:
		sys.exit('Reference database does not exist')	

	# Connect to the database in which the timeline will be stored
	# If the same database as the users then just reference it here
	db_tl = db_users
	# try:
	# 	db_tl = couch[database_tl]
	# except Exception, e:
	# 	db_tl = couch.create(database_tl)

	"""
	Set up the twitter connections
	"""
	#set the keys
	consumer_key, consumer_secret, access_token_key, access_token_secret = set_keys(keyfile)

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token_key, access_token_secret)

	# If using the REST API then use this constructor
	api = tweepy.API(auth)

	"""
	Continually cycle through the database
	Pull down users timelines and store in the specified database
	"""
	try:
		while True:
			#cycle through the reference database

			count = 0

			for row in db_users.view('_design/general/_view/user_id_view', group = True):

				user_id = row.key

				process_user(api, user_id, db_tl)

				print 'Processed user_id %s' %(user_id)

				## process each of the followers
				# followers = api.followers(user_id = user_id)

				# for follower in followers:

				# 	if follower._json['location'] == 'Brisbane':

				# 		follower_id = follower._json['id']

				# 		process_user(api, follower_id, db_tl)

				#  		print 'Processed user_id %s: follower_id %s' %(user_id, follower_id)

	except KeyboardInterrupt:
		print '\nKeyboard Interrupt\nShutting down the harvester'	

#Check if the user has already been processed, then add the tweets to the database
def process_user(api, user_id, db):
	#store the user_id to save extra datbase lookups
	try:
		user_statuses = api.user_timeline(id = user_id, count = 200)
		add_tweets_to_db(user_statuses, db)
	#throws errors if the user has a protected timeline
	except Exception, e:
		pass

#Add the tweet to the database
def add_tweets_to_db(statuses, db):
	for status in statuses:
		try:
			if status.place.full_name == location:
				if status.id_str not in db:
					tweet = status._json
					#Override the default _id assignment
					tweet['_id'] = status.id_str

					#Add document to the datbase
					#We could check if its there before we add it
					#but this will be slower as it is an extra
					#connecion to the database and try/except handles this anyway
					try:
						db.save(tweet)
						print 'Tweet added to CouchDB: %s' %(tweet.text)
					
					#It will get upset if its already there so just pass
					#as we need to add it anyway
					except Exception, e:
						pass

		#May not have a place or a full name...
		except AttributeError:
			#skip that tweet
			pass

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