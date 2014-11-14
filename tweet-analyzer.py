###############################################################################
#	File: tweet-analyzer.py
#	Authors: Daniel Fahey and Ian Smith
#	For: CSE489 - Big Data Project, NMT Fall 2014
#	Project Purpose:
#		Collect tweets from given users and store any that are 'directed' in a
#		mongoDB database. Directed tweets are those that tag other twitter users
#		by using the @ symbol. 
#		Then, analyze these tweets for various 'positive' and 'negative' words,
#		creating a possible friendship score. The frequency of tweets also
#		affects the score, so that people who only sent 1 or 2 tweets are not 
#		considered best friends or worst enemies.
#
#	File Description:
#		tweet-analyzer.py pulls all of the relevant tweets for the given user
# 		or user pair and examines them, calculating a 'friendship' score based
#		on the content of the tweets.
###############################################################################

import pymongo, argparse, sys

# Construct the arguments for this script.
parser = argparse.ArgumentParser(description = 'Analyze the tweets for a given user or user pair and calculate a "friendship" score.')
parser.add_argument('-u1', '--user1', help = 'Choose twitter user 1. This is required.', required = True)
parser.add_argument('-u2', '--user2', help = 'Choose twitter user 2', default = '')
parser.add_argument('-d', '--db', help = 'MongoDB URI. This is required.', required = True)

args = parser.parse_args()
user1 = args.user1
user2 = args.user2
dburi = args.db

# Attempt to connect to the database.
try: 
	conn = pymongo.MongoClient(dburi)
except:
	print 'Error: Unable to connect to DB.'
	sys.exit()
uri_parts = pymongo.uri_parser.parse_uri(dburi)
db = conn[uri_parts['database']]

# Process for a user pair
if user2 is not '':
	collection = user1+'_'+user2
	print 'Examining tweets from the '+collection+' collection.'
	tweets = db.collection.find().toArray()
	size = db[collection].find().size()
	i = 0
	while i < size:
		print 'Tweet = "'+tweet[i]+'".'

# Process for a single user	
else:
	#TODO
	sys.exit()