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

import pymongo, argparse, sys, textblob

# Construct the arguments for this script.
parser = argparse.ArgumentParser(description = 'Analyze the tweets for a given user or user pair and calculate a "friendship" score.')
parser.add_argument('-d', '--db', help = 'MongoDB URI. This is required.', required = True)

args = parser.parse_args()
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
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
# Create the Bayes analyzer
ana = NaiveBayesAnalyzer()
todo = open('collectionNames.txt','r')
todo = 
# analyze the tweets
if user2 is not '':
	collection = db[user1+'_'+user2]
	print 'Examining tweets from the '+user1+'_'+user2+' collection.'
	tweets = collection.find()
	fval = 0
	counter = 0
	for tweet in tweets:
		#print 'Tweet = "'+tweet["text"]+'".'
		blob = TextBlob(tweet["text"], analyzer=ana)
		if blob.sentiment.classification is 'pos':
			tval = 0.5
		else:
			tval = -0.5
		fval += tval + (blob.sentiment.p_pos - blob.sentiment.p_neg)
		counter += 1
		print tweet["text"]

	fval = fval * counter / 10
	print 'Score = ' + str(fval) + ', out of ' + str(counter) + ' tweets'
# Process for a single user	
else:
	#TODO
	sys.exit()
