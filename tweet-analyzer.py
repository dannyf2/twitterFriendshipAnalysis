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
# open the file with all of the functions
todo = open('collectionNames.txt','r')
# loop line by line and calculate scores for each
valList = []
colstring = todo.readline()
while len(colstring) is not 0:
	colstring = colstring.replace('\n','')
	users = colstring.split(',')
	# analyze the tweets
	collection = db[users[0]+'_'+users[1]]
	print 'Examining '+users[0]+' and '+users[1]+'.'
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
		#print tweet["text"]

	fval = fval * counter
	valList.append([users[0],users[1],fval])
	colstring = todo.readline()
	
# push everything to a file
outfile = open('scores.txt','w')
for val in valList:
	print >> outfile, str(val[0]) + "," + str(val[1]) + "," + str(val[2])
