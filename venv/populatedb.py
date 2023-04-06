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
 
    # Call Analysis API /audio-analysis/:id
    response = requests.get(url, auth=BearerAuth(spotify_token))
    res = response.json()
    return res

def get_spotify_id(song_info, limit = 1):
    #spotify_token = os.environ.get('spotify_api_token')

    query = "?q={}&artist={}&type=track&limit={}".format(song_info[0], song_info[1], limit)
    url = os.environ.get('SPOTIFY_BASE_URL') + query


    if("#" in url):  # check that url doesnt have # chars
        print(url)
        index = url.find('#')
        url = url[:index] + "%23" + url[index+1:]
        print("found that #")
        print(url)

    response = requests.get(url, auth=BearerAuth(spotify_token))
    json_data = response.json()


    if(url == "https://api.spotify.com/v1/search?q=There's A Star Spangled Banner Waving #2 (The Ballad Of Francis Powers)&artist=Red River Dave&type=track&limit=1"):
        return 0

    try:
        if json_data['tracks']['items'] == []:   # skip over 
            return 0
    except:
        auth_manager.get_cached_token()
        #spotify_token = auth_manager.get_access_token(as_dict=False)
        print("failed")
        print(url)
        print(json_data)

    #try:
    #    if json_data['tracks']['items'] == []:   # skip over 
    #        return 0
    #except:
    #    print(json_data)

    
    if json_data['tracks']['items'] == []:   # skip over 
        print(json_data)
        return 0
    
    

    id_string = json_data['tracks']['items'][0]['uri']
    id = id_string[14:]

    return id

# investigate theses dates
#1980-08-24 
#1981-02-01
#====
#1983-07-31
#1983-12-18
# They are missing from data set maybe issue with billboard API? 



def generate_dates():   # restart from 1980-08-17
    dates_gen= pd.date_range("10-16-2005","03-22-2023",freq='W').tolist()
    dates = []
    for d in dates_gen:  
        dates.append(d.strftime('%Y-%m-%d')[:10])
    return dates

def get_ids(week_top_100, song_id,id_song, id_songartist):
    catch_count = 0
    week_ids =[]
    for song in week_top_100:    # get top track ids for given week
        trackid = 0
        if song[0] in song_id:
            catch_count += 1
            week_ids.append(song_id[song[0]])   # if we already have the song and id skip look up

        else:       # check the dict if track already exists
            trackid = get_spotify_id(song)  

        if trackid != 0:
            week_ids.append(trackid) 
            song_id[song[0]] = trackid
            id_song[trackid] = song[0]
            id_songartist[trackid] = song[1]
    
    return week_ids,song_id,id_song,id_songartist,catch_count/100

def add_songs_mongo(db,list_of_dicts,id_song,id_songartist):
    songs = db['songs']
    
    for dictionary in list_of_dicts['audio_features']:
        if(type(dictionary) == type(None)):
            print(dictionary)
            print("nonetype")
            break
        spotify_id = dictionary['id']
        if songs.find_one({"id":spotify_id}):
            continue
        
        mongo_post = {}
        mongo_post["name"] = id_song[spotify_id]
        mongo_post["artist"] = id_songartist[spotify_id]
        for key in dictionary:
            if key in ['type','uri','track_href','analysis_url']:
                continue
            else:
                mongo_post[key] = dictionary[key]

        result = songs.insert_one(mongo_post)

        if result.acknowledged:
            print("Inserted " + id_song[spotify_id])
        else:
            print("Insertion failed")

def add_weeks_mongo(db,date,ids):
    weeks = db['weeks']
    mongo_post = {}
    mongo_post["date"] = date
    mongo_post["ids"] = ids

    result = weeks.insert_one(mongo_post)
    
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
song_id = {}
id_song = {}
id_songartist = {}
db = client['MHA']


testids = "7LHKJdWpQ4JkmMFWGwVjnV,3XKIUb7HzIF1Vu9usunMzc,2ctvdKmETyOzPb2GiJJT53,2ctvdKmETyOzPb2GiJJT53,6qc34bnVOyqGDPni8H5W0U,62bOmKYxYg7dhrC6gH9vFn,3BsaRV5QIulYz2lV9WWa8T,0AcLrSfAEBQcUnHOTm5pXg,5z6xHjCZr7a7AIcy8sPBKy,5s4catxeZsaWFnOrvrXZHf,5Mmk2ii6laakqfeCT7OnVD,6dJ2mSRaKE9ctYw9qWNGWQ,6nozDLxeL0TE4MS9GqYU1v,4Y8q64VnhD0vFYy9g2WFpi"


for date in dates:  

    week_top_100 = get_list(list, date)          # retrieve list of top 100 songs and artists

    week_ids, song_id,id_song,id_songartist,catch_rate = get_ids(week_top_100,song_id,id_song,id_songartist)   # retrieve spotify track ids 
    print(date + " " + str(catch_rate))


    string_of_ids =','.join(week_ids)

    res = get_analysis_features(string_of_ids)                      # get musical features for all songs that week

    add_weeks_mongo(db,date,week_ids)
    add_songs_mongo(db,res,id_song,id_songartist)

    db['songs']

    #week_dict = {'date':date, 'songs':week_ids}
    #print(week_dict)
    song_dict = {}





