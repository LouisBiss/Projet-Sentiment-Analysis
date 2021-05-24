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
import pandas as pd 
import csv


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
        type_analyse=request.form['type_analyse']
        
        #Si le type d'analyse 'global' est sélectionné
        
        if type_analyse=='global':
            
            
            tweets=tweepy.Cursor(api.search, q=Mot_clef_recherche, lang="en").items(Nb_tweets)
  
            
            tweets_positifs_total=0
            tweets_negatifs_total=0
            tweets_neutre_total =0
                

            for tweet in tweets:
                analysis=TextBlob(tweet.text)
                polarity=analysis.sentiment.polarity
                #print(tweet.text)
             
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
                  
                #sauvegarde l'image pour la réutiliser dans l'html
                plt.savefig('static/images/new_plot.png')
        
                
                return render_template('base.html', a='tweets positifs:{}'.format(positive_per)+' %',
                                        b='tweet négatifs:{}'.format(negative_per)+' %',
                                        c='tweets neutres:{}'.format(neutral_per)+' %')
                #return render_template('base.html', b='tweet négatifs:{}'.format(negative_per)+' %')
                #return render_template('base.html', c='tweets neutres:{}'.format(neutral_per)+' %')


        #Si une analyse par source est choisie 

        elif type_analyse=='source':
            
            tweets = tweepy.Cursor(api.search, q=Mot_clef_recherche, lang="en").items(Nb_tweets)

            for tweet in tweets:
                url  =  f"https://twitter.com/{ tweet . user . id}/status/{ tweet . id }"
    
    
                def get_all_tweets(screen_name):
                    # Twitter only allows access to a users most recent 3240 tweets with this method
                
                
                    tweets = tweepy.Cursor(api.search, q=Mot_clef_recherche, lang="en").items(Nb_tweets)
                    
                    # transform the tweepy tweets into a 2D array that will populate the csv
                    outtweets = [[tweet.id, tweet.user.name, tweet.created_at, tweet.text, tweet.geo, tweet.user.location, tweet.user.followers_count, tweet.source] for tweet in tweets]
                
                    # write the csv
                    with open('tweets.csv', 'w', encoding='utf-8') as f:
                        writer = csv.writer(f, delimiter=';', quotechar='`')
                        writer.writerow(["Id", "user", "created_at", "text", "géo", "location", "Followers", "source"])
                        writer.writerows(outtweets)
                     
                
                if __name__ == '__main__':
                    # pass in the username of the account you want to download
                    get_all_tweets("J_tsar")
                
                try:
                    tweets_data = pd.read_csv('tweets.csv', skiprows=[0])
                    pd.set_option('display.max_columns', None)
                except:
                    pass     #outrepasse les erreurs dans le csv
                    
                 
                #lecture csv
                df=pd.read_csv("tweets.csv", sep=";", error_bad_lines=False)
    
    
                #retire les lignes erronées
                df=df[df.Id.apply(lambda x: x.isnumeric())]  #retire toute les ou il y a une erreur 
                df.drop_duplicates(subset="Id",inplace=True) #on s'assure qu'il n'y a pas de doublons
                
                #nettoyage tweet
                df['text']=df['text'].str.replace('(@\w+.*?)',"")  #retire les @
                df['text'] = df['text'].str.replace('http\S+|www.\S+', "") #retire les url
                
                    
                #Ajuste la dénomitaiton des sources pourque cela soit plus lisible sur les graphes
                replacement = {
                    "Twitter for ": "",   #remplace par rien => efface
                    "Twitter ": "",        #ne pas oublier d'ajouter un espace à la fin
                    #"***: "***"
                }
                df['source']=df['source'].replace(replacement, regex=True)
                
                #Remplace toutes les autres sources minoritaires par 'Autre'
                x = ['iPhone', 'Android', 'Web App', 'iPad']  #liste des éléments à conserver
                df['source']=df['source'].apply(lambda i: i if i in x else 'Autre')
                
                #Analyse sentimentale du texte des tweets 
                df['polarité'] = df['text'].apply(lambda text: TextBlob(text).sentiment.polarity)
                
                #Simplifications des résultats pour être plus lisible
                polarité_neutre = df["polarité"]== 0
                polarité_positive = df["polarité"] > 0
                polarité_negative = df["polarité"] < 0
                
                df.loc[polarité_neutre, "polarité"]= 'neutre'
                df.loc[polarité_positive, "polarité"]= 'positive'
                df.loc[polarité_negative, "polarité"]= 'négative'
                
                
                #Création d'un nouveau dataframe avec seulement la source et la polarité
                df_pol_par_source=df[['source','polarité']]
                
                #get dummies polarité, permettra de faire la somme de chaque polarité en fonction de la source
                df_pol_par_source = pd.get_dummies(df_pol_par_source, columns = ['polarité'])
                
                #aggreagation, fusion et somme des lignes de meme source
                aggregation_functions = {'polarité_neutre': 'sum', 'polarité_négative': 'sum','polarité_positive':'sum'}
                df_pol_par_source = df_pol_par_source.groupby(df['source']).aggregate(aggregation_functions)
                
                #fait les sommes du nombre du tweets par sources, pour le calcul des pourcentages à venir
                df_pol_par_source["sum"] = df_pol_par_source.sum(axis=1)
                
                #Calcul du pourcentage de chaque polarité par tweet
                df_pol_par_source['polarité_neutre'] = df_pol_par_source['polarité_neutre'].astype(int) 
                df_pol_par_source['polarité_positive'] = df_pol_par_source['polarité_positive'].astype(int) 
                df_pol_par_source['polarité_négative'] = df_pol_par_source['polarité_négative'].astype(int) 
                
                df_pol_par_source['polarité_neutre'] =((df_pol_par_source['polarité_neutre'] * 100)/ df_pol_par_source['sum'])
                df_pol_par_source['polarité_positive'] =((df_pol_par_source['polarité_positive'] * 100)/ df_pol_par_source['sum'])
                df_pol_par_source['polarité_négative'] =((df_pol_par_source['polarité_négative'] * 100)/ df_pol_par_source['sum'])
                
                #On retire la colonne 'sum' afin de faire le tableau
                df_pol_par_source=df_pol_par_source.drop(columns=['sum'])
                
                
                #Diagramme en barres par source
                df_pol_par_source.plot.bar(rot=0)
                
                #sauvegarde image
                plt.savefig('static/images/new_plot.png')


        elif type_analyse=='abonnés':
            
            #création csv
            tweets = tweepy.Cursor(api.search, q=Mot_clef_recherche, lang="en").items(Nb_tweets)
            for tweet in tweets:
    
                url  =  f"https://twitter.com/{ tweet . user . id}/status/{ tweet . id }"
    
    
                def get_all_tweets(screen_name):
                    # Twitter only allows access to a users most recent 3240 tweets with this method
                
                
                    tweets = tweepy.Cursor(api.search, q=Mot_clef_recherche, lang="en").items(Nb_tweets)
                    
                    # transform the tweepy tweets into a 2D array that will populate the csv
                    outtweets = [[tweet.id, tweet.user.name, tweet.created_at, tweet.text, tweet.geo, tweet.user.location, tweet.user.followers_count, tweet.source] for tweet in tweets]
                
                    # write the csv
                    with open('tweets.csv', 'w', encoding='utf-8') as f:
                        writer = csv.writer(f, delimiter=';', quotechar='`')
                        writer.writerow(["Id", "user", "created_at", "text", "géo", "location", "Followers", "source"])
                        writer.writerows(outtweets)
                     
                
                if __name__ == '__main__':
                    # pass in the username of the account you want to download
                    get_all_tweets("J_tsar")
                
                try:
                    tweets_data = pd.read_csv('tweets.csv', skiprows=[0])
                    pd.set_option('display.max_columns', None)
                except:
                    pass
                    
                 
                #lecture csv
                df=pd.read_csv("tweets.csv", sep=";", error_bad_lines=False)
    
    
                #retire les lignes erronées
                df=df[df.Id.apply(lambda x: x.isnumeric())]  #retire toute les ou il y a une erreur 
                df.drop_duplicates(subset="Id",inplace=True) #on s'assure qu'il n'y a pas de doublons
                
                #nettoyage tweet
                df['text']=df['text'].str.replace('(@\w+.*?)',"")  #retire les @
                df['text'] = df['text'].str.replace('http\S+|www.\S+', "") #retire les url
                
                #On transforme tout les valeurs du nombres de followers en numéric, certain étant caractérisé par "Nan" ou autre, étant donné qu'il s'agit de compte privé.
                #On les remplaces par -1 afin de facilement les compter comme "inconnu" plus tard.
                df['Followers'] = pd.to_numeric(df.Followers, errors='coerce').fillna(-1)
                
                #Création d'un nouveau dataframe avec seulement les données nous interréssant 
                df_nbfol=df[['Followers','polarité']]
                df_nbfol = pd.get_dummies(df_nbfol, columns = ['polarité'])
                
                #Création des conditions de tries
                moins_10=(df_nbfol.Followers >= 0) & (df_nbfol.Followers <=10)
                moins_50=(df_nbfol.Followers > 10) & (df_nbfol.Followers <=50)
                moins_100=(df_nbfol.Followers >50) & (df_nbfol.Followers <=100)
                moins_500=(df_nbfol.Followers >100) & (df_nbfol.Followers <=500)
                moins_1000=(df_nbfol.Followers >500) & (df_nbfol.Followers <=1000)
                plus_1000=(df_nbfol.Followers >1000)
                inconnu=(df_nbfol.Followers <0)
                
                #Remplace le nombre d'abonnés selon les conditions
                colonne="Followers"
                df_nbfol.loc[moins_10, colonne] = 'Moins de 10 followers'
                df_nbfol.loc[moins_50, colonne] = 'Moins de 50 followers'
                df_nbfol.loc[moins_100, colonne] = 'Moins de 100 followers'
                df_nbfol.loc[moins_500, colonne] = 'Moins de 500 followers'
                df_nbfol.loc[moins_1000, colonne] = 'Moins de 1000 followers'
                df_nbfol.loc[plus_1000, colonne] = 'Plus de 1000 followers'
                df_nbfol.loc[inconnu, colonne] = 'Compte privé'
                
                #Aggreation
                aggregation_functions_2 = {'polarité_neutre': 'sum', 'polarité_négative': 'sum','polarité_positive':'sum'}
                df_nbfol = df_nbfol.groupby(df_nbfol['Followers']).aggregate(aggregation_functions_2)
                
                #Somme de chaque catégories
                df_nbfol["sum"] = df_nbfol.sum(axis=1)
                
                #Calcul pourcentage 
                df_nbfol['polarité_neutre'] = df_nbfol['polarité_neutre'].astype(int) 
                df_nbfol['polarité_positive'] = df_nbfol['polarité_positive'].astype(int) 
                df_nbfol['polarité_négative'] = df_nbfol['polarité_négative'].astype(int) 
                
                df_nbfol['polarité_neutre'] =((df_nbfol['polarité_neutre'] * 100)/ df_nbfol['sum'])
                df_nbfol['polarité_positive'] =((df_nbfol['polarité_positive'] * 100)/ df_nbfol['sum'])
                df_nbfol['polarité_négative'] =((df_nbfol['polarité_négative'] * 100)/ df_nbfol['sum'])
                
                df_nb_fol=df_nbfol.drop(columns=['sum'])
                
                #affiche diagramme
                df_nbfol.plot.bar(rot=0)
                
                plt.savefig('static/images/new_plot.png')

if __name__=="__main__":
    app.run(debug=True)