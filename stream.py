# -*- coding: utf-8 -*-

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json
import sys
import requests
from datetime import datetime
#from WConio import *

OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

class StdOutListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        #key = tweet.keys()
        #print(key)
        #print(tweet)
        if "friends" in tweet:
            print(tweet)
            #key = tweet.keys()
            #print(key)
            return True
        else:
            #print(repr(tweet['text']))
            #key = tweet.keys()
            #print(key)
            #print(tweet)
            if not "text" in tweet:
                if "delete" in tweet:
                    print("Tweet Deleted:" + str(tweet['delete']['status']['id']))
                    return True

                print(tweet)
                return True

            if "RT" in tweet['text'].encode("utf-8","ignore").decode("utf-8",'xmlcharrefreplace'):
                print(ENDC+"Retweeted from "+OKGREEN+tweet['user']['name'].encode("utf-8","ignore").decode("utf-8",'xmlcharrefreplace') +ENDC+ "("+OKBLUE+"@" + tweet['user']['screen_name']+ENDC+")"+":\n"+tweet['text'].encode("utf-8","ignore").decode("utf-8",'xmlcharrefreplace'))
                return True
            #print(tweet['text'])
            print(ENDC+"Tw from:"+OKGREEN+tweet['user']['name'].encode("utf-8","ignore").decode("utf-8",'xmlcharrefreplace')+ENDC+"("+OKBLUE+"@"+tweet['user']['screen_name']+ENDC+"), \n"+WARNING+tweet['text'].encode("utf-8","ignore").decode("utf-8",'xmlcharrefreplace'))
            if "こんばんは" in tweet['text']:
                if tweet['user']['screen_name'] not in myself.screen_name:
                    time = datetime.now()
                    api.update_status('@'+tweet['user']['screen_name'] +" こんばんはぁー 現在の時刻は " + time.strftime('%Y年%m月%d日、%H時%M分%S秒') + "です！",tweet['id'])
                    return True

            return True
#        if data.startswith("{"):
#            print(data)
        return True

    def on_error(self, status):
        print(status)

    def disconnect(self):
        if self.running is False:
            return False
        self.running = False

if __name__ == '__main__':
    f = open('twitterkey.json','r')
    #print(f)
    fl = json.load(f)
    #print(fl)
    l = StdOutListener()
    r = requests
    CONSUMER_KEY = fl['consumer_key']
    CONSUMER_SECRET = fl['consumer_key_secret']
    f.close()
    icecastserver = ""
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    #print(fl['access_token'])
    if fl['access_token'] != None:
        f = open('twitterkey.json','r')
        ACCESS_TOKEN = fl['access_token']
        ACCESS_SECRET = fl['access_token_secret']
        f.close()

    else:
        redirect_url = auth.get_authorization_url()
        print (redirect_url)
        verifier = input('Type the verification code: ').strip()
        auth.get_access_token(verifier)
        ACCESS_TOKEN = auth.access_token
        ACCESS_SECRET = auth.access_token_secret
        fl['access_token'] = ACCESS_TOKEN
        fl['access_token_secret'] = ACCESS_SECRET
        f = open('twitterkey.json','w')
        f.writelines(json.dumps(fl))
        f.close()

    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    myself = api.me()
    stream = Stream(auth, l)
    stream.userstream(async=True)
    #stream.filter(async=True)
    while True:
        s = input()
        args = s.split(" ",1)
        if "tweet" in args[0]:
            if args[1] != None:
                api.update_status(args[1])
                continue

        if "die" in args[0]:
            stream.disconnect()
            print("exitted!")
            sys.exit()

        if "showme" in args[0]:
            print(api.me().screen_name)

        if "icecast_setserver" in args[0]:
            if not "" in args[1]:
                print(args[1])
                icecastserver = args[1]

        if "icecastnp" in args[0]:
            req_url = icecastserver + "/status-json.xsl"
            print(icecastserver)
            icecast_json = json.loads(r.get(req_url))
            args = s.split(" ")
            np = icecast_json['icecast']['source'][int(args[1])]['title']
            server_name = icecast_json['icecast']['source'][int(args[1])]['server_name']
            api.update_status("Now playing at " + server_name + ", " + title + "!")

