# Run the following commands to start the server...
# . venv/bin/activate             Activates the virtual environment
# flask run -p 8000 --host 0.0.0.0         Starts the server

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
import math

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

def convert_ms(ms):
    seconds_duration = ms / 1000

    # Calculate minutes and remaining seconds
    minutes = seconds_duration // 60
    remaining_seconds = seconds_duration % 60

    # Create a dictionary with minutes and seconds
    duration_dict = {'minutes': int(minutes), 'seconds': round(remaining_seconds)}

    # Calculate the decimal minutes
    decimal_minutes = round(seconds_duration / 60, 2)

    return_value = [duration_dict, decimal_minutes]
    return return_value

app = create_app()

if __name__ == '__main__':
    app.run(port=8000)

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

HOST = 'http://localhost:3000'

# Only here for test purposes
@app.route("/")
def hello_world():
    hello = "Hello world"
    return hello

@app.route("/query", methods=['GET'])
def query():

    def print_query(start_date, end_date, interval):
        print("Querying for dates... START:", start_date, "END", end_date, "on a", interval, "interval")

    if request.method == 'GET':
        try:
            start_date_str = request.args.get('startDate')
            end_date_str = request.args.get('endDate')
            
            if len(end_date_str) != 10 or len(start_date_str) != 10:
                raise ValueError("Invalid date format")
            
            interval = request.args.get('interval')

            if interval == 'Week':
                aggregate_type = 'week_aggregate_top_100'
                interval_print_option = 'weeks sent.'
                number_option = 'week_number'
            elif interval == 'Month':
                aggregate_type = 'month_aggregate_top_100'
                interval_print_option = 'months sent.'
                number_option = 'month_number'
            elif interval == 'Year':
                aggregate_type = 'year_aggregate_top_100'
                interval_print_option = 'years sent.'
                number_option = 'year_number'
            else:
                raise ValueError("Invalid interval")

            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

            print_query(start_date, end_date, interval)

            pipeline = [     
                    {
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
            values = db[aggregate_type].aggregate(pipeline)
            count = 0

            averages = {
                "acousticness": 0,
                "danceability": 0,
                "energy":0,
                "instrumentalness": 0,
                "liveness": 0,
                "speechiness": 0,
                "valence": 0
            }

            for doc in values:
                # [0] => Duration Dictionary, [1] => Duartion min in float
                ms_conversion = convert_ms(doc['duration_ms'])

                doc['duration_min_sec'] = ms_conversion[0]
                doc['duration_min_decimal'] = ms_conversion[1]

                del doc['date_field']

                dictionary = {}
                dictionary['data'] = doc

                # Add current summation for each key
                for key in averages.keys():
                    averages[key] += doc[key]

                # Add current week/month/year count
                dictionary[number_option] = count

                data.append(dictionary)
                count +=1

            # Average certain keys
            for key in averages.keys():
                averages[key] = round(averages[key]/count,2)

            response_dictionary = {
                'result_data_array': data,
                'averages': averages,
            }

            response = jsonify(response_dictionary)
            response.headers.add('Access-Control-Allow-Origin', HOST)

            print(len(data), interval_print_option)
            
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
            
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

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

            songs_collection = db['songs']

            for track in data['tracks']:
                info = {}
                info['artist'] = track["album"]["artists"][0]["name"]
                info['song'] = track["name"]
                info["image_url"] = track["album"]["images"][0]["url"]
                info["id"] = track["id"]

                song_analysis = songs_collection.find_one({'id': track['id']})

                key = song_analysis['key']
                mode = song_analysis['mode']

                info['key'] = key
                info['mode'] = mode
                info['key_mode_pair'] = f"{key}_{mode}"
                response.append(info)


            response = jsonify(response)
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')

            return response
                

        except Exception as e:
            print("ERROR:", e)
            return e