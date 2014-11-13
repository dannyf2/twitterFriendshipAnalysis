import argparse, os 

# argument definitions
parser = argparse.ArgumentParser(description = 'Wrapper for the various features of the Twitter Friendship Analysis program.')
parser.add_argument('-th', '--twitterharvest', help = 'harvest tweets for user1', action = 'store_true')
parser.add_argument('-r', '--relationship', help = 'calculate the relationship between the two users', action = 'store_true')
parser.add_argument('-u1', '--user1', help = 'choose twitter user', default = 'dannyf2')
parser.add_argument('-u2', '--user2', help = 'choose twitter user', default = 'mongolab')
parser.add_argument('-nodb', '--nodatabase', help = 'stops the twitter harvest from using the database. Use for debugging purposes.', action = 'store_true')
parser.add_argument('-max', '--maxtweets', help = 'sets the maximum limit on the number of tweets to be harvested.', default = 0);

# grab the arguments
args = parser.parse_args()
harv = args.twitterharvest
rel = args.relationship
user1 = args.user1
user2 = args.user2
nodb = args.nodatabase
maxtweets = args.maxtweets


# execute twitter-harvest.py
if harv == True:
	#construct the arguments
	consumerkey = " --consumer-key ffj33PQt2HZnliUnk4yigfDAJ"
	consumersec = " --consumer-secret 9VdoozAio9mcE3zQO70Q9TjRAVQTvwFLXWmGAkwU2EiDmn3Qh2"
	acctoken = " --access-token 203190168-V7Yr9LQ95w2WD7Pli5r1DyBsfboUXlQhxmhtrcAH"
	accsec = " --access-secret 7cgCzHJNwQFVUdL0zYIegqOimLNhgsPjAZVs9fhCZqVpP"
	userarg = " --user " + user1
	if nodb == True:
		mongoarg = ""
	else:
		mongoarg = " --db mongodb://localhost:27017/testdb"
	if maxtweets is not 0:
		limitarg = " --numtweets " + str(abs(int(maxtweets)))
	else:
		limitarg = ""
	print 'Running twitter harvester for '+user1+'.'
	os.system("python twitter-harvest.py" + consumerkey + consumersec + acctoken + accsec + userarg + mongoarg)

# compute the relationship between the two users
if rel == True:
	print 'Calculating the relationship between '+user1+' and '+user2+'.'
	# TODO
	
if harv==False and rel==False:
	print 'Use -th for twitter harvesting or -r for calculating relationships.'
