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
dates = generate_dates()

missing_dates = []
for week in client['MHA']['weeks'].find():
    if len(week['ids']) < 99 :
        #print(str(week['date']) + " " + str(len(week['ids'])))
        missing_dates.append(week['date'])

#missing_dates = ['1980-08-24', '1980-08-31', '1980-09-07', '1980-09-14', '1980-09-21', '1980-09-28', '1980-10-05', '1980-10-12', '1980-10-19', '1980-10-26', '1980-11-02', '1980-11-09', '1980-11-16', '1980-11-23', '1980-11-30', '1980-12-07', '1980-12-14', '1980-12-21', '1980-12-28', '1981-01-04', '1981-01-11', '1981-01-18', '1983-07-31', '1983-08-07', '1983-08-14', '1983-08-21', '1983-08-28', '1983-09-04', '1983-09-11', '1983-09-18', '1983-09-25', '1983-10-02', '1983-10-09', '1983-10-16', '1983-10-23', '1983-10-30', '1983-11-06', '1983-11-13', '1983-11-20', '1983-11-27', '1983-12-04', '1983-12-11']

print(missing_dates)
#for date in missing_dates:
    #ls = get_list('hot-100',date)
    #print(ls)


#print(client['MHA']['songs'].find_one({"artist":"shasdfsaf"}))
#if not client['MHA']['songs'].find_one({"artist":"shasdfsaf"}):
#    print("nonetpye")


#for date in missing_dates:
#    ids = client['MHA']['weeks'].find_one({"date" : date})["ids"]

#    for id in ids:
       # print(client['MHA']['songs'].find_one({"id" : id})['name'])
#        if not client['MHA']['songs'].find_one({"id" : id}):
#            print("missing : " + id)

