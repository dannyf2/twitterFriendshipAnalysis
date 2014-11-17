###############################################################################
#
# Copyright (c) 2013 ObjectLabs Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
###############################################################################

###############################################################################
#	File: twitter-harvest.py
#	Modification Authors: Daniel Fahey and Ian Smith
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
#		twitter-harvest.py is used to collect the directed tweets for specific 
#		users and store them into a mongoDB database. Thanks to ObjectLabs for 
#		the permission to use this software.
###############################################################################

__author__ = 'mongolab'


import pymongo
import oauth2 as oauth
import urllib2, json
import sys, argparse, time 

def oauth_header(url, consumer, token):

    params =  {'oauth_version': '1.0',
    'oauth_nonce': oauth.generate_nonce(),
    'oauth_timestamp': int(time.time()),
    }
    req = oauth.Request(method = 'GET',url = url, parameters = params)
    req.sign_request(oauth.SignatureMethod_HMAC_SHA1(),consumer, token)
    return req.to_header()['Authorization'].encode('utf-8')

def main():

    ### Build arg parser
    parser = argparse.ArgumentParser(description = 'Connects to Twitter User Timeline endpoint, retrieves tweets and inserts into a MongoDB database. Developed on Python 2.7')
    parser.add_argument('-r', '--retweet', help = 'include native retweets in the harvest', action = 'store_true')
    parser.add_argument('-v', '--verbose', help = 'print harvested tweets in shell', action = 'store_true')
    parser.add_argument('--numtweets', help = 'set total number of tweets to be harvested, max = 3200', type = int, default = 3200)
    parser.add_argument('--user', help = 'choose twitter user timeline for harvest', default = 'mongolab')
    parser.add_argument('--db', help = 'MongoDB URI, example: mongodb://dbuser:dbpassword@dbhnn.mongolab.com:port/dbname')
    parser.add_argument('--consumer-key', help = 'Consumer Key from your Twitter App OAuth settings', required = True)
    parser.add_argument('--consumer-secret', help = 'Consumer Secret from your Twitter App OAuth settings', required = True)
    parser.add_argument('--access-token', help = 'Access Token from your Twitter App OAuth settings', required = True)
    parser.add_argument('--access-secret', help = 'Access Token Secret from your Twitter App Dev Credentials', required = True)
    parser.add_argument('--until-date', help = 'note date to harvest until in mmmddyyyy format were month is months 3 letter equivalent', required = False, default = 'jan112014')

    ### Fields for query
    args = parser.parse_args()
    user = args.user 
    numtweets = args.numtweets
    verbose = args.verbose
    retweet = args.retweet
    endDate = args.until_date

    if endDate != '':
       endMon = endDate[:3]
       endDay = endDate[3:5]
       endYear = endDate[5:9]

    ### Build Signature
    CONSUMER_KEY = args.consumer_key
    CONSUMER_SECRET = args.consumer_secret
    ACCESS_TOKEN = args.access_token
    ACCESS_SECRET = args.access_secret

    ### Build Endpoint + Set Headers
    base_url = url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?include_entities=true&count=200&screen_name=%s&include_rts=%s' % (user, retweet)
    oauth_consumer = oauth.Consumer(key = CONSUMER_KEY, secret = CONSUMER_SECRET)
    oauth_token = oauth.Token(key = ACCESS_TOKEN, secret = ACCESS_SECRET)

    ### Setup MongoLab Goodness
    uri = args.db
    if uri != None:
        try: 
            conn = pymongo.MongoClient(uri)
            print 'Harvesting...'
        except:
            print 'Error: Unable to connect to DB. Check --db arg'
            return
        uri_parts = pymongo.uri_parser.parse_uri(uri)
        db = conn[uri_parts['database']]
        db['twitter-harvest'].ensure_index('id_str')

    ### Helper Variables for Harvest
    max_id = -1
    tweet_count = 0

    targetList = []
    relationshipList = []

    ### Begin Harvesting
    while True:
        auth = oauth_header(url, oauth_consumer, oauth_token)
        headers = {"Authorization": auth}
        request = urllib2.Request(url, headers = headers)
        try:
            stream = urllib2.urlopen(request)
        except urllib2.HTTPError, err:
            if err.code == 404:
                print 'Error: Unknown user. Check --user arg'
                return
            if err.code == 401:
                print 'Error: Unauthorized. Check Twitter credentials'
                return
        tweet_list = json.load(stream)

        if len(tweet_list) == 0:
            print 'No tweets to harvest!'
            return
        if 'errors' in tweet_list:
            print 'Hit rate limit, code: %s, message: %s' % (tweets['errors']['code'], tweets['errors']['message'])
            return
        if max_id == -1:
            tweets = tweet_list
        else:
            tweets = tweet_list[1:]
            if len(tweets) == 0:
                print 'Finished Harvest!'

				###add unique names found as well as relationships to file 
                targetList.sort()
                f = open('toCollect.txt', 'a+')
                for name in targetList:
                    print >> f, name  # or f.write('...\n')
                f.close()
                f = open('collectionNames.txt', 'a+')
                for relation in relationshipList:
                    print >> f, relation  # or f.write('...\n')
                f.close()
                return
        for tweet in tweets:
            max_id = id_str = tweet['id_str']
            try:
                if tweet_count == numtweets:
                   print 'Finished Harvest- hit numtweets!' 
                   targetList.sort()
                   f = open('toCollect.txt', 'a+')
                   for name in targetList:
                       print >> f, name  # or f.write('...\n')
                   f.close()
                   f = open('collectionNames.txt', 'a+')
                   for relation in relationshipList:
                       print >> f, relation  # or f.write('...\n')
                   f.close()
                   return
                dateCreated = tweet['created_at']
                monthCreated = dateCreated[4:7]
                dayCreated = dateCreated[8:10]
                yearCreated = dateCreated[-4:]
                if int(yearCreated) < int(endYear):
                   print 'Finished Harvest- hit year end'
                   targetList.sort()
                   f = open('toCollect.txt', 'a+')
                   for name in targetList:
                       print >> f, name  # or f.write('...\n')
                   f.close()
                   f = open('collectionNames.txt', 'a+')
                   for relation in relationshipList:
                       print >> f, relation  # or f.write('...\n')
                   f.close()
                   return 
                for x in range(0, len(tweet['entities']['user_mentions'])):
                    target = tweet['entities']['user_mentions'][x]['screen_name']
                    if targetList.count(target) ==0:
                        targetList.append(target)
                    if relationshipList.count(user +"," +target) ==0:
                        relationshipList.append(user +","+target)
                    if uri != None:
                        db[user + '_' + target].update({'id_str':id_str},tweet,upsert = True)
                    else:
                        print tweet['entities']['user_mentions'][x]['screen_name']
                        #print tweet['created_at']
                tweet_count+=1
                if verbose == True and uri != None:
                    print tweet['text']
            except Exception, err:
                print 'Unexpected error encountered: %s' %(err)
                return    
        url = base_url + '&max_id=' + max_id 

if __name__ == '__main__':
    try:
        main()
    except SystemExit as e:
        if e.code == 0:
            pass
