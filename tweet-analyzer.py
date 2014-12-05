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

import pymongo, argparse, sys, textblob, pickle, os

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
from textblob.classifiers import NaiveBayesClassifier

if os.path.isfile('anafile') is True:
	anafile = open('anafile','rb')
	ana = pickle.load(anafile)
	anafile.close()
else:
	# Create the Bayes analyzer
	print 'Loading naive bayes classifier, this may take a few moments...'
	ana = NaiveBayesClassifier(open('trainingSet.txt','r'),format="csv")
	anafile = open('anafile','wb')
	pickle.dump(ana,anafile)
	anafile.close()
	
print 'Getting accuracy...'
print 'accuracy = ' + str(ana.accuracy(open('testingSet.txt','r'),format="csv"))
	
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
	for tweet in tweets:
		#print 'Tweet = "'+tweet["text"]+'".'
		text = tweet["text"]
		#remove all of the @handles
		s = text.find('@')
		while s is not -1:
			e = text.find(' ',s)
			if e is -1:
				r = text[s:]
			else:
				r = text[s:e]
			text = text.replace(r,'')
			s = text.find('@')
		#end while
		#remove the hashtags
		text = text.replace('#','')
		text = text.lstrip()
		prob = ana.prob_classify(text)
		print ana.classify(text)
		if prob.max() is 'pos':
			val = 1
		else:
			val = -1
		#val = (round(prob.prob("pos"),2) - round(prob.prob("neg"),2))
		fval += val
		#print text
		#print str(val)
	
	#end for
	print 'final = '+str(fval)
	#fval = fval * counter
	valList.append([users[0],users[1],fval])
	colstring = todo.readline()
#end while
# push everything to a file
outfile = open('scores.txt','w')
for val in valList:
	print >> outfile, str(val[0]) + "," + str(val[1]) + "," + str(val[2])
