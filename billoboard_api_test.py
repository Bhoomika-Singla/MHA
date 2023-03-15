import billboard
import requests
import os
from dotenv import load_dotenv

load_dotenv()

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

def get_spotify_id(song_info, limit = 1):
    spotify_token = os.environ.get('spotify_api_token')

    query = "?q={}&artist={}&type=track&limit={}".format(song_info[0], song_info[1], limit)

    url = os.environ.get('SPOTIFY_BASE_URL') + query

    response = requests.get(url, auth=BearerAuth(spotify_token))
    json_data = response.json()
    print(json_data)
    id_string = json_data['tracks']['items'][0]['uri']
    print(id_string)
    print(id_string[14:])
    id = id_string[14:]

    return id

def get_analysis_features(song_id):

    base_url = os.environ.get('SPOTIFY_BASE_URL')

    # Call Analysis API /audio-analysis/:id

    song_analysis = {}

    # Call Features API /audio-features/:id

    song_features = {}



    song_info ={
        song_analysis: song_analysis,
        song_features: song_features,
    }

    return song_info

# def main():

list = 'hot-100'
date = '1950-03-22'

test_list = get_list(list, date)
get_spotify_id(test_list[0])
# print(test_list)







