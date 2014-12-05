import argparse, sys

# argument definitions
parser = argparse.ArgumentParser(description = 'Small program used to reconfigure the dataset to a better format.')
parser.add_argument('-f', '--file', help = 'dataset file', default='')


# grab the arguments
args = parser.parse_args()
filename = args.file

f = open(filename,'r')
w = open('trainingSet.txt','w')
t = open('testingSet.txt','w')

counter = 0

for line in f:
	if counter is not 0:
		words = line.split(',')
		if int(words[1]) is 1:
			sen = 'pos'
		else: 
			sen = 'neg'
		i = 3
		tweet = ''
		while i < len(words):
			tweet += words[i]
			i += 1
		tweet = tweet.replace('\n','')
		s = tweet.find('@')
		while s is not -1:
			e = tweet.find(' ',s)
			if e is -1:
				r = tweet[s:]
			else:
				r = tweet[s:e]
			tweet = tweet.replace(r,'')
			s = tweet.find('@')
			
		newl = tweet + ',' + sen + '\n'
		newl = newl.lstrip()
		#print(newl)
		#print newline[0] + newline[1] + newline[2]
		if counter >= 500:
			w.write(newl)
		else:
			t.write(newl)
	counter += 1
	if counter > 5000:
		break
print (str(counter))
