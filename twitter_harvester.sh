#!/bin/bash
#

#update the installer
#sudo apt-get update

#install couchdb
#sudo apt-get install couchdb -y

#install pip
#sudo apt-get install python-pip
#easy_install -U pip

#install python Daemon
#sudo apt-get install python-daemon

#install python modules
#sudo pip install tweepy
#sudo pip install CouchDB

python twitter_harvester1.py auth.txt couchDB.txt 'http://115.146.95.216:5984/' 'brisbanetweets' '152.81,-27.75,153.24,-27.11'

