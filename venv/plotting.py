import billboard
import datetime
import requests
import spotipy
import pandas as pd
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


