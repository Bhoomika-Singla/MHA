import billboard
import datetime
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from statistics import mode as modefunc

import pymongo
import pprint
import os
from bson.objectid import ObjectId

load_dotenv()

conn_str = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.8.0"
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
try:
    print(client.server_info()['version'])
except Exception:
    print("unable to connect to server")

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)
spotify_token = auth_manager.get_access_token(as_dict=False)


# create week aggregates of song feature data

# need to do this manually


weeks = client['MHA']['weeks']
songs = client['MHA']['songs']
week_aggregate_top_100 = client['MHA']['week_aggregate_top_100']
week_aggregate_top_10 = client['MHA']['week_aggregate_top_10']
week_aggregate_top_1 = client['MHA']['week_aggregate_top_1']


count = 0
for week in weeks.find():

    if week_aggregate_top_1.find_one({"date":week['date']}):
        print("already exists")
        continue
    
    ids = week['ids']
    agg_post = {}

    keyls = []
    mode = []
    time_signature = []

    features = ['danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms','time_signature']
    special_features = ['key','mode','time_signature']
    count = 0

   #print(week['date'])

    for id in ids[:1]:
        #print(id)
        song = songs.find_one({"id":id})
        if not song:
            continue
        count += 1
        for key in features:
            value = song[key]
            if key == 'key':
                keyls.append(value) 
                continue
            if key ==  'mode':
                mode.append(value)
                continue
            if key == 'time_signature':
                time_signature.append(value)
                continue
            
            if key not in agg_post:
                agg_post.update({key:value})
            agg_post[key] += value


    #print(agg_post)

    try:
        for key in agg_post:
            agg_post[key] = round(agg_post[key]/count,2)
        if len(keyls) > 0:
            keyls_mode = modefunc(keyls) 
        if len(mode) > 0:
            mode_mode = modefunc(mode)
        if len(time_signature) > 0:
            time_signature_mode = modefunc(time_signature)

        agg_post.update({"date":week['date']})
        agg_post.update({"key":keyls_mode})
        agg_post.update({"mode":mode_mode})
        agg_post.update({"time_signature":time_signature_mode})

        week_aggregate_top_1.insert_one(agg_post) 


    except:
        print(week["date"])
        continue






        



