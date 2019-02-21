import tweepy
import sys
import json
from tweepy import OAuthHandler
from textwrap import TextWrapper
from datetime import datetime
from elasticsearch import Elasticsearch

consumer_key = ""
consumer_secret = ""
access_token = ""
access_secret = ""

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

es = Elasticsearch([{'host':'localhost', 'port':9200}])
es.indices.create(index='twitterdata_5',ignore=400)

class StreamApi(tweepy.StreamListener):
    status_wrapper = TextWrapper(width=60, initial_indent='  ', subsequent_indent='  ')

    def on_status(self, status):

           json_data = status._json

           es.index(index='twitterdata_5',
                     doc_type='twitter',
                     body=json_data,
                     ignore=400
                     )
streamer = tweepy.Stream(auth=auth, listener=StreamApi(), timeout=30)


terms = ['Roger Stone', 'roger stone']

streamer.filter(None, terms)
