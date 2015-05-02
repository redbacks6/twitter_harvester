# twitter_harvester
Python script for harvesting tweets using the twitter API and pushing to a couchDB database

# Command line arguments
The best way to run the script is to use the bash script and change the command line arguments to suit

The command line arguments are as follows:
1) location of space deliminated text file containing twitter authorisation tokens
2) location of space deliminated text file containing couchDB username and password
3) couchDB IP and Port as a string
4) name of the database as a string
5) coordinates of the bounding box for tweets that you want to capture. Enter coordinates as a string - i.e. '152.81,-27.75,153.24,-27.11'

# Setting up the environment
I've entered comments into the bash script with directions on how to set up the environment on a VM

# Running on VM
I have been running using screen. It let you close the SSH connection without stopping the script.

Direction on how to use screen are here (or easily accessible via a cheeky google search)
http://askubuntu.com/questions/8653/how-to-keep-processes-running-after-ending-ssh-session
