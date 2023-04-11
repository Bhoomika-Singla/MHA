import billboard
import datetime
import requests
import spotipy
import pprint
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


weeks = client['MHA']['weeks']
songs = client['MHA']['songs']
week_aggregate_top_100 = client['MHA']['week_aggregate_top_100']
week_aggregate_top_10 = client['MHA']['week_aggregate_top_10']
week_aggregate_top_1 = client['MHA']['week_aggregate_top_1']

tables = [weeks,week_aggregate_top_100,week_aggregate_top_10,week_aggregate_top_1]

for table in tables:
    for week in table.find():
        date = week['date']
        year = date[:4]
        month = date[5:7]
        day = date[8:10]

        #print (year + " " + month + " " + day)

        try : # check if new fields have been added
            week['year']
            week['month']
            week['date']
        except: # if it hasn't add the new fields
            print(date + " has not been updated")
            table.update_one({"_id":week["_id"]}, {"$set": {"year": year}})
            table.update_one({"_id":week["_id"]}, {"$set": {"month": month}})
            table.update_one({"_id":week["_id"]}, {"$set": {"day": day}})
     
