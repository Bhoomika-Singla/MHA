import billboard
import datetime
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

import pymongo
import pprint
import os
from bson.objectid import ObjectId

import pandas as pd

load_dotenv()

conn_str = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.8.0"
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
try:
    print(client.server_info()['version'])
except Exception:
    print("unable to connect to server")


def get_list(list, date):
    songs = []
    chart = billboard.ChartData(list, date=date)

    for i in chart.entries:
        name = i.title
        artist = i.artist
        songs.append((name, artist))

    return songs

def generate_dates():   # restart from 1980-08-17
    dates_gen= pd.date_range("10-16-2005","03-22-2023",freq='W').tolist()
    dates = []
    for d in dates_gen:  
        dates.append(d.strftime('%Y-%m-%d')[:10])
    return dates


#print(get_list('hot-100',"2005-07-24"))


# test for dates misssing lists
db = client['MHA']
weeks = db['weeks']
songs = db['songs']
dates = generate_dates()

missing_ids = []

for week in weeks.find():
    for id in week['ids']:
        if not songs.find_one({"id":id}):
            missing_ids.append(id)

    #ls = get_list('hot-100',date)
    #print(ls)

print(missing_ids)

#print(client['MHA']['songs'].find_one({"artist":"shasdfsaf"}))
#if not client['MHA']['songs'].find_one({"artist":"shasdfsaf"}):
#    print("nonetpye")


#for date in missing_dates:
#    ids = client['MHA']['weeks'].find_one({"date" : date})["ids"]

#    for id in ids:
       # print(client['MHA']['songs'].find_one({"id" : id})['name'])
#        if not client['MHA']['songs'].find_one({"id" : id}):
#            print("missing : " + id)

