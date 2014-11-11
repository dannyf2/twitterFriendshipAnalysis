import argparse, os 

# argument definitions
parser = argparse.ArgumentParser(description = 'Wrapper for the various features of the Twitter Friendship Analysis program.')
parser.add_argument('-th', '--twitterharvest', help = 'harvest tweets for user1', action = 'store_true')
parser.add_argument('-r', '--relationship', help = 'calculate the relationship between the two users', action = 'store_true')
parser.add_argument('-u1', '--user1', help = 'choose twitter user', default = 'mongolab')
parser.add_argument('-u2', '--user2', help = 'choose twitter user', default = 'mongolab')

# grab the arguments
args = parser.parse_args()
harv = args.twitterharvest
rel = args.relationship
user1 = args.user1
user2 = args.user2


# execute twitter-harvest.py
if harv == True:
	print 'Running twitter harvester for '+user1+'.'
	os.system("python twitter-harvest.py --consumer-key ffj33PQt2HZnliUnk4yigfDAJ --consumer-secret 9VdoozAio9mcE3zQO70Q9TjRAVQTvwFLXWmGAkwU2EiDmn3Qh2 --access-token 203190168-V7Yr9LQ95w2WD7Pli5r1DyBsfboUXlQhxmhtrcAH --access-secret 7cgCzHJNwQFVUdL0zYIegqOimLNhgsPjAZVs9fhCZqVpP --user " + user1)

# compute the relationship between the two users
if rel == True:
	print 'Calculating the relationship between '+user1+' and '+user2+'.'
	# TODO
	
if harv==False and rel==False:
	print 'Use -th for twitter harvesting or -r for calculating relationships.'
