# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 11:23:43 2021

@author: louis
"""

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
api = tweepy.API(auth)

Mot_clef_recherche=input("Entrer le mot clef ou hastag de votre recherche: ")
Nb_tweets=int(input("Entrer le nombre de tweets à analyser: "))

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

print("Pourcentage de tweets positifs:" +str(positive_per))
print("Pourcentage de tweets negatifs:" +str(negative_per))
print("Pourcentage de tweets neutres:" +str(neutral_per))


'''per_tweet = ['Positif'+str(positive_per),'Neutre'+str(neutral_per),'Negatif'+str(negative_per)]
per_total =[0,100]
plt.plot(per_tweet,per_total)

plt.show()'''

left = [1,2,3]
  
# heights of bars
height = [int(positive_per),int(neutral_per),int(negative_per)]
  
# labels for bars
tick_label = ['Positif', 'Neutre', 'Négatif']
  
# plotting a bar chart
plt.bar(left, height, tick_label = tick_label,
        width = 0.8, color = ['green', 'orange','red'])
  
# naming the x-axis
plt.xlabel('Polarité')
# naming the y-axis
plt.ylabel('Pourcentages')
# plot title
plt.title('Analyse Sentimentale de "'+str(Mot_clef_recherche)+'" sur ' + str(Nb_tweets)+' tweets')
  
# function to show the plot
plt.show()

