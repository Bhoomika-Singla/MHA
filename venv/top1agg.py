from flask import Flask, request, jsonify
import pymongo
import numpy as np
import spotipy
import requests
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime
from collections import Counter
import os
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# connect to mongodb 
client = pymongo.MongoClient(f"mongodb+srv://BigDataUser:{os.environ.get('MONGO_PASS')}@bigdatamhacluster.cu0olpo.mongodb.net/?retryWrites=true&w=majority", serverSelectionTimeoutMS=5000)
db = client['MHA'] # Accessed by `flask.current_app.db`

#db['week_aggregate_top1'].drop()

pipeline = [     {
        "$addFields":{
            "date_field":{
                "$dateFromString":{
                    "dateString": "$date",
                    "format":"%Y-%m-%d"
                }
            }
        }
    },
    {
        "$match":{
            "date_field":{
                "$gte": datetime(2000,1,1),
            }
        }
    },
    {   
        "$project":{
            "_id": 0,  "ids": 1, "date":1
        }
    },
    {
        "$sort":{
            "date_field":1
        }
    }
    ]

values = db['weeks'].aggregate(pipeline)


for doc in values:
    print(doc['date'] + " " +doc['ids'][0])

    if db['week_aggregate_top1'].find_one({"date":doc["date"]}):
       print("skipped" + "  " + doc['date']) 
       continue   

    try :
        newpost = {}
        newpost['date'] = doc['date']
        features = db['songs'].find_one({"id":doc['ids'][0]})
        for x in features:
            if x == '_id':
                continue
            newpost[x] = features[x]

        print("adding  " + newpost['date'])
        db['week_aggregate_top1'].insert_one(newpost)
    
    except:
        print("missed  " + doc["date"] + "   " + doc["ids"][0])
        continue


    #print("missed " + doc['ids'][0])
    
    
