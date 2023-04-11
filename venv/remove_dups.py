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
        pipeline = [
            {"$match":{"date":week['date']}}
        ]

        count = len(list(table.aggregate(pipeline=pipeline)))
        if(count > 1):
            print(week["date"] + " " + str(count))
            table.delete_one({"date":week["date"]})

        #pprint.pprint(list(weeks.aggregate(pipeline=pipeline)))
