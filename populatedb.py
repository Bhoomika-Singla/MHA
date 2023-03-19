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

conn_str = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.8.0"
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
try:
    print(client.server_info()['version'])
except Exception:
    print("unable to connect to server")

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


def get_analysis_features(song_ids):

    url = "https://api.spotify.com/v1/audio-features?ids="+song_ids
    #print(url)
 
    # Call Analysis API /audio-analysis/:id
    
    response = requests.get(url, auth=BearerAuth(spotify_token))
    return response.json()
    

def get_spotify_id(song_info, limit = 1):
    #spotify_token = os.environ.get('spotify_api_token')

    query = "?q={}&artist={}&type=track&limit={}".format(song_info[0], song_info[1], limit)
    url = os.environ.get('SPOTIFY_BASE_URL') + query
    response = requests.get(url, auth=BearerAuth(spotify_token))
    json_data = response.json()

    if json_data['tracks']['items'] == []:   # skip over 
        return 0

    id_string = json_data['tracks']['items'][0]['uri']
    id = id_string[14:]

    return id

def generate_dates():
    dates_gen= pd.date_range("03-22-2000","03-22-2023",freq='W').tolist()
    dates = []
    for d in dates_gen:  
        dates.append(d.strftime('%Y-%m-%d')[:10])
    return dates

def get_ids(week_top_100, all_ids):
    catch_count = 0
    week_ids =[]
    for song in week_top_100:    # get top track ids for given week
        trackid = 0
        if song[0] in all_ids:
            catch_count += 1
            week_ids.append(all_ids[song[0]])   # if we already have the song and id skip look up

        else:       # check the dict if track already exists
            trackid = get_spotify_id(song)  

        if trackid != 0:
            week_ids.append(trackid) 
            all_ids[song[0]] = trackid
    
    return week_ids,all_ids, catch_count/100

def add_songs_mongo(db,list_of_dicts):

    songs = db['songs']

    for dictionary in list_of_dicts['audio_features']:
        spotify_id = dictionary['id']
        if songs.find_one({"id":spotify_id}):
            print(id + " exists")
        else:
            print("adding doc")

        mongo_post = {}
        for key in dictionary:
            if key in ['type','uri','track_href','analysis_url']:
                continue
            else:
                mongo_post[key] = dictionary[key]

        result = songs.insert_one(mongo_post)

        if result.acknowledged:
            print("Insertion successful")
        else:
            print("Insertion failed")

    
def get_aggregate(list_of_dicts):
    result_dict = {}
    for dictionary in list_of_dicts['audio_features']:
        for key in dictionary:

            if key in ['type','uri','track_href','analysis_url','id']:
                continue
            if key not in result_dict:
                result_dict[key] = dictionary[key]
            else:
                result_dict[key] += dictionary[key]


    for key in result_dict:
        result_dict[key] = result_dict[key] / len(list_of_dicts['audio_features'])

    return result_dict
 #========================================================================

dates = generate_dates()
list = 'hot-100'
all_ids = {}


testids = "7LHKJdWpQ4JkmMFWGwVjnV,3XKIUb7HzIF1Vu9usunMzc,2ctvdKmETyOzPb2GiJJT53,6qc34bnVOyqGDPni8H5W0U,62bOmKYxYg7dhrC6gH9vFn,3BsaRV5QIulYz2lV9WWa8T,0AcLrSfAEBQcUnHOTm5pXg,5z6xHjCZr7a7AIcy8sPBKy,5s4catxeZsaWFnOrvrXZHf,5Mmk2ii6laakqfeCT7OnVD,6dJ2mSRaKE9ctYw9qWNGWQ,6nozDLxeL0TE4MS9GqYU1v,4Y8q64VnhD0vFYy9g2WFpi"
res = get_analysis_features(testids)

print(res['audio_features'][1]['id'])
print(type(res))

#week_aggregate = get_aggregate(res)
#print(week_aggregate)

add_songs_mongo(client['test'],res)


for date in dates[:1]:  

    week_top_100 = get_list(list, date)          # retrieve list of top 100 songs and artists
        
    week_ids, all_ids, catch_rate = get_ids(week_top_100, all_ids)   # retrieve spotify track ids 
    print(date + " " + str(catch_rate))

        
    string_of_ids =','.join(week_ids)

    res = get_analysis_features(string_of_ids)                      # get musical features for all songs that week


    week_dict = {'date':date, 'songs':week_ids}
    
    #print(week_dict)
    song_dict = {}

post = {

}

print("soungcount " + str(len(all_ids))) 



