#!/bin/bash
#

#update the installer
#sudo apt-get update

#install couchdb
#sudo apt-get install couchdb -y

#install screen
#sudo apt-get install screen

#install pip
#sudo apt-get install python-pip
#easy_install -U pip

#install python modules
#sudo pip install tweepy
#sudo pip install CouchDB

#auth.txt is a space deliminated text file with the four twitter authorisations
#couchdb.txt is a space deliminated text file with the username and password for the couchDB database

python twitter_harvester.py auth.txt couchDB.txt 'http://115.146.95.161:5984/' 'brisbane_cleaned' '152.81,-27.75,153.24,-27.11'

