# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 12:48:18 2021

@author: louis
"""

import tweepy
from tweepy import OAuthHandler
"""from textblob import textblob
from wordcloud import WordlCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pylot as plt    #permet de faire des graphe 
plt.style.use('fivethirtyeight')"""

from tweepy.streaming import StreamListener
from tweepy import Stream 

#charger les données 

consumer_key = 'dySQaiuzfk6WSVGPEiCeXCpYI'
consumer_secret = 'S2YJ4Banm0BVmtpxvyrVXomrfEjLQ6dtjqjqV8kBfnIf1W2n9W'
access_token = '1373575730697801735-7KxHpiw4YEYRz7ND2elLvqE8ys6mup'
access_secret = 'NHzt2cJpaP83hcUDgtoCH22oOmzOX7p8nY83TUjvyeM7m'

class myStreamlistener (StreamListener):
                def on_data(self, data):
                    print (data) 
                    return True 
                def on_error (self, status):
                    print (status)


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
twitterStream = Stream(auth,myStreamlistener())
twitterStream.filter(track=["football"])
api = tweepy.API(auth)
