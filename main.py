###############################################################################
#	File: main.py
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
#		main.py is simply a wrapper file so that users only need to execute 1
#		python script in order to use the various features of this project.
###############################################################################

import argparse, os, sys

# argument definitions
parser = argparse.ArgumentParser(description = 'Wrapper for the various features of the Twitter Friendship Analysis program.')
parser.add_argument('-th', '--twitterharvest', help = 'harvest tweets for user1', action = 'store_true')
parser.add_argument('-r', '--relationship', help = 'calculate the relationship between the two users (or all of the relationships for 1 user)', action = 'store_true')
parser.add_argument('-u1', '--user1', help = 'choose twitter user 1', default = '')
parser.add_argument('-u2', '--user2', help = 'choose twitter user 2', default = '')
parser.add_argument('-nodb', '--nodatabase', help = 'stops the twitter harvest from using the database. Use for debugging purposes.', action = 'store_true')
parser.add_argument('-max', '--maxtweets', help = 'sets the maximum limit on the number of tweets to be harvested.', default = 0);
parser.add_argument('-s', '--seed', help = 'sets flag indicating the -u1 parameter is the seed user.', default = 0);

# grab the arguments
args = parser.parse_args()
harv = args.twitterharvest
rel = args.relationship
user1 = args.user1
user2 = args.user2
nodb = args.nodatabase
maxtweets = args.maxtweets
seed = args.seed

# global key values
#construct the arguments
consumerkey = ' --consumer-key ffj33PQt2HZnliUnk4yigfDAJ'
consumersec = ' --consumer-secret 9VdoozAio9mcE3zQO70Q9TjRAVQTvwFLXWmGAkwU2EiDmn3Qh2'
acctoken = ' --access-token 203190168-V7Yr9LQ95w2WD7Pli5r1DyBsfboUXlQhxmhtrcAH'
accsec = ' --access-secret 7cgCzHJNwQFVUdL0zYIegqOimLNhgsPjAZVs9fhCZqVpP'

if seed == True:
	
# execute twitter-harvest.py
if harv == True:
	if user1 is not '':
		userarg = ' --user ' + user1
	else:
		print 'Must define user1 in order to harvest tweets. (use -u1 <username>)'
		sys.exit()
	if nodb == True:
		mongoarg = ''
	else:
		mongoarg = ' --db mongodb://localhost:27017/testdb'
	if maxtweets is not 0:
		limitarg = ' --numtweets ' + maxtweets
	else:
		limitarg = ''
	print 'Running twitter harvester for '+user1+'.'
	#execute the python script
	os.system('python twitter-harvest.py' + consumerkey + consumersec + limitarg + acctoken + accsec + userarg + mongoarg)
	#sys.exit()

# execute tweet-analyzer.py
if rel == True:
	#construct the arguments
	if user1 is not '':
		user1arg = ' -u1 ' + user1
	else:
		print 'Must define user1 in order to run analysis. (use -u1 <username>)'
		sys.exit()
	if user2 is not '':
		user2arg = ' -u2 ' + user2
		print 'Calculating the relationship between '+user1+' and '+user2+'.'
	else:
		user2arg = ''
		print 'Calculating the relationships for '+user1+'.'
	mongoarg = ' --db mongodb://localhost:27017/testdb'
	#execute the python script
	os.system('python tweet-analyzer.py' + user1arg + user2arg + mongoarg)
	sys.exit()
	
if harv==False and rel==False:
	print 'Use -th for twitter harvesting or -r for calculating relationships. Use -h for more info.'
	sys.exit()
