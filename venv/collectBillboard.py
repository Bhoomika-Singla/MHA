import billboard
import datetime
import pandas as pd
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

import pymongo
import pprint
import os
from bson.objectid import ObjectId

load_dotenv()

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)
spotify_token = auth_manager.get_access_token(as_dict=False)


#=========================================================================
class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

def get_list(list, date):
    songs = []
    chart = billboard.ChartData(list, date=date)
    for i in chart.entries:
        name = i.title
        artist = i.artist
        songs.append((name, artist))
    return songs

def generate_dates():
    dates_gen= pd.date_range("03-22-1940","03-22-2023",freq='W').tolist()
    dates = []
    for d in dates_gen:  
        dates.append(d.strftime('%Y-%m-%d')[:10])
    return dates


dates = generate_dates()
list = 'hot-100'
print(len(dates))

file = open("billboard.txt", "w")

for date in dates[:3]:
    
    file.write(date)
    songs = get_list(list,date)
    for song in songs:
        file.write(song[0])
        file.write(song[1])
    
    print(str)




