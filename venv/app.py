# Run the following commands to start the server...
# . venv/bin/activate             Activates the virtual environment
# flask --app app.py run          Starts the server

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

def create_app():
    app = Flask(__name__)
    cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    return app


def get_available_weeks(db):
    weeks = []

    for week in db['weeks'].find(): # Iterates over all weeks
        date = week['date']

        weeks.append(datetime.strptime(date, '%Y-%m-%d').date())

    return np.sort(weeks)

def get_available_months(db):
    months = []

    for agg_obj in db['month_aggregate_top_100'].find():
        # Setting day as 1 for comparison purposes
        months.append(datetime(year=agg_obj['year'], month=agg_obj['month'], day = 1).date())

    return np.sort(months)

app = create_app()

# Load environment variables
load_dotenv()

# connect to mongodb 
client = pymongo.MongoClient(f"mongodb+srv://BigDataUser:{os.environ.get('MONGO_PASS')}@bigdatamhacluster.cu0olpo.mongodb.net/?retryWrites=true&w=majority", serverSelectionTimeoutMS=5000)
db = client['MHA'] # Accessed by `flask.current_app.db`

#connect to spotify API
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)
spotify_token = auth_manager.get_access_token(as_dict=False)

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


available_weeks = get_available_weeks(db) # Accessed by flask.current_app.available_dates

if __name__ == 'main':
    app.run()

# Only here for test purposes
@app.route("/")
def hello_world():
    hello = "Hello world"
    return hello

@app.route("/query", methods=['GET'])
def query():
    if request.method == 'GET':
        try:

            start_date_str = request.args.get('startDate')
            end_date_str = request.args.get('endDate')
            
            if len(end_date_str) != 10 or len(start_date_str) != 10:
                raise ValueError("Invalid date format")
            
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            interval = request.args.get('interval')

            print("Querying for dates... START:", start_date, "END", end_date, "on a", interval, "interval")

            if interval == 'Week':
                week_agg_collection = db['week_aggregate_top_100']
                week_counter = 0
                weeks_data = []
                for date in available_weeks:
                    print(date)
                    if date >= start_date:
                        week_data = week_agg_collection.find_one({'date': datetime.strftime(date, '%Y-%m-%d')})
                        del week_data['_id']
                        weeks_data.append(
                            {
                                'week_number': week_counter,
                                'data': week_data
                            }
                        )
                        week_counter += 1
                    if date > end_date:
                        break

                print(len(weeks_data), "Weeks sent")
                return jsonify(weeks_data)
                
            elif interval == 'Month':
                month_agg_collection = db['month_aggregate_top_100']
                month_counter = 0
                months_data = []

                available_months = get_available_months(db)
                
                for date in available_months:
                    if date >= start_date:
                        month_data = month_agg_collection.find_one({'month': date.month, 'year': date.year})
                        del month_data['_id']
                        months_data.append({
                            'month_number': month_counter,
                            'data': month_data
                        })
                        month_counter += 1
                    if date > end_date:
                        break

                print(len(months_data), 'months sent.')
                return jsonify(months_data)
            elif interval == 'Year':
                year_agg_collection = db['year_aggregate_top_100']
                year_counter = 0
                years_data = []

                for year in range(start_date.year, end_date.year + 1):
                    year_data = year_agg_collection.find_one({'year': year})
                    del year_data['_id']
                    years_data.append(
                        {
                            'year_number': year_counter,
                            'data': year_data
                        }
                    )
                    year_counter += 1

                print(len(years_data), 'years sent.')
                return jsonify(years_data)

            else:
                raise ValueError("Invalid interval")
        except Exception as e:
            print("ERROR:", e)
            return e
        

# required fields   'startDate':'YYYY-MM-DD'   
#                   'endDate':'YYYY-MM-DD'  
#                   'interval' :'week' or 'month' or 'year'
# note the date can be 'YYYY-MM' or just 'YYYY'  as long as 'month' 'year' 'week'
# granularity is specified
# DON'T use top1
@app.route("/query2", methods=['GET'])
def query2():
    if request.method == 'GET':
        try:
            start_date_str = request.args.get('startDate')
            end_date_str = request.args.get('endDate')
            interval = request.args.get('interval')
            top_count = request.args.get('topCount')

            if(interval == 'week'):
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

            if(interval == 'month'):
                start_date = datetime.strptime(start_date_str, "%Y-%m")
                end_date = datetime.strptime(end_date_str, "%Y-%m")

            if(interval == 'year'):
                start_date = datetime.strptime(start_date_str, "%Y")
                end_date = datetime.strptime(end_date_str, "%Y")

            #if len(end_date_str) != 10 or len(start_date_str) != 10:
            #    raise ValueError("Invalid date format")

            if(top_count == 'top100'):
                collection = db['week_aggregate_top_100']
            if(top_count == 'top10'):
                collection = db['week_aggregate_top_10']
            if(top_count == 'top1'):
                collection = db['week_aggregate_top1']
                


            #print("Querying for dates... START:", start_date, "END", end_date, "on a", interval, "interval")
         
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
                        "$gte": start_date,
                        "$lte": end_date,
                    }
                }
            },
            {   
                "$project":{
                    "_id": 0,  "danceability": 1, 'energy': 1, 'loudness': 1, 'speechiness': 1, 'acousticness': 1, 'instrumentalness': 1, 'liveness': 1, 'valence': 1, 'tempo': 1, 'duration_ms': 1, 'date': 1, 'key': 1, 'mode': 1, 'time_signature': 1, 'year': 1, 'month': 1, 'day': 1, 'date_field': 1
                }
            },
            {
                "$sort":{
                    "date_field":1
                }
            }
            ]

            data = []
            values = collection.aggregate(pipeline)

            count = 1
            for doc in values:
                print(doc)
                del doc['date']
                del doc['date_field']
                if(top_count != 'top1'):
                    del doc['day']
                    del doc['month']
                    del doc['year']
                dictionary = {}
                dictionary['data'] = doc
                dictionary['week_number'] = count
                data.append(dictionary)
                count +=1

            response = jsonify(data)
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
            return response


        except Exception as e:
            print("ERROR:", e)
            return e


# required fields   'startDate':'YYYY-MM-DD'   'endDate':'YYYY-MM-DD'  'songCount':int 
@app.route("/top_songs", methods=['GET'])
def top_songs():
    if request.method == 'GET':
        try: 
            
            start_date_str = request.args.get('startDate')
            end_date_str = request.args.get('endDate')
            song_count = request.args.get('songCount')

            if len(end_date_str) != 10 or len(start_date_str) != 10:
                raise ValueError("Invalid date format")
            
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")#.date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")#.date()

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
                        "$gte": start_date,
                        "$lte": end_date,
                    }
                }
            },
            {
                "$sort":{
                    "date_field":1
                }
            }
            ]

            values = db['weeks'].aggregate(pipeline=pipeline)
            top_ids_count = []
            for doc in values:
                top_ids_count.append(doc['ids'][0])
            
            c = []
            c = Counter(top_ids_count)
            #print(c.most_common(int(song_count)))
            top_ids = [t[0] for t in c.most_common(int(song_count))]
            url = "https://api.spotify.com/v1/tracks"

            string_of_ids =','.join(top_ids)

            params = {
                'ids': string_of_ids
            }

            data = requests.get(url,params,auth=BearerAuth(spotify_token))
            data = data.json()

            response = []
        
            count = 1
            for track in data['tracks']:
                #print(track["album"]["artists"][0]["name"])
                #print(track["name"])
                #print(track["album"]["images"][0]["url"])
                info = {}
                info['artist'] = track["album"]["artists"][0]["name"]
                info['song'] = track["name"]
                info["image_url"] = track["album"]["images"][0]["url"]
                info["id"] = track["id"]
                response.append(info)


            response = jsonify(response)
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')

            return response
                

        except Exception as e:
            print("ERROR:", e)
            return e