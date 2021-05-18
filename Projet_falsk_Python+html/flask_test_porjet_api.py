# -*- coding: utf-8 -*-
"""
Created on Wed May 12 19:34:03 2021

@author: louis
"""
#pour lancer la page, copier l'adresse dans le navigateur: http://localhost:5000/

import tweepy 
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt

#charger les données 

consumer_key = 'dySQaiuzfk6WSVGPEiCeXCpYI'
consumer_secret = 'S2YJ4Banm0BVmtpxvyrVXomrfEjLQ6dtjqjqV8kBfnIf1W2n9W'
access_token = '1373575730697801735-7KxHpiw4YEYRz7ND2elLvqE8ys6mup'
access_secret = 'NHzt2cJpaP83hcUDgtoCH22oOmzOX7p8nY83TUjvyeM7m'

#Authentification

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
#api = tweepy.API(auth)
api = tweepy.API(auth, wait_on_rate_limit=True)  #à utiliser en cas d'erreur 432

from flask import Flask, render_template, url_for,request
from subprocess import run,PIPE


app = Flask(__name__,template_folder='templates')



@app.route('/')
def index():
    return render_template('base.html')

@app.route('/send', methods=['POST'])
def send():
    if request.method == 'POST':
        Mot_clef_recherche = request.form['mot_clef']
        
        Nb_tweets = request.form['nb_tweet']
        Nb_tweets=float(Nb_tweets)

        tweets=tweepy.Cursor(api.search, q=Mot_clef_recherche, lang="fr").items(Nb_tweets)
        
        tweets_positifs_total=0
        tweets_negatifs_total=0
        tweets_neutre_total =0
            
            
        for tweet in tweets:
            analysis=TextBlob(tweet.text)
            polarity=analysis.sentiment.polarity
         
            #print (tweet.text)
            #analysis = TextBlob(tweet.text)
            #print (analysis.sentiment)
            
            if (analysis.sentiment.polarity>0):
                tweets_positifs_total+=1
            elif(analysis.sentiment.polarity<0):
                tweets_negatifs_total+=1
            elif(analysis.sentiment.polarity==0):
                tweets_neutre_total+=1
                
                
        positive_per = (tweets_positifs_total*100)/Nb_tweets
        negative_per = (tweets_negatifs_total*100)/Nb_tweets
        neutral_per = (tweets_neutre_total*100)/Nb_tweets
        
        return render_template('base.html', a='tweets positifs:{}'.format(positive_per)+' %',
                                b='tweet négatifs:{}'.format(negative_per)+' %',
                                c='tweets neutres:{}'.format(neutral_per)+' %')
        #return render_template('base.html', b='tweet négatifs:{}'.format(negative_per)+' %')
        #return render_template('base.html', c='tweets neutres:{}'.format(neutral_per)+' %')

      
if __name__=="__main__":
    app.run(debug=True)