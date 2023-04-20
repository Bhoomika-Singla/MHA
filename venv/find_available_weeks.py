import pymongo
import numpy as np

client = pymongo.MongoClient("mongodb+srv://BigDataUser:MusicHistoryAnalyzer@bigdatamhacluster.cu0olpo.mongodb.net/?retryWrites=true&w=majority", serverSelectionTimeoutMS=5000)
db = client['MHA']

songs_collection = db['songs']
weeks_collection = db['weeks']
weeks_avg_collection = db["weeks-average"]

blank_feature_arrays = {
    'danceability': [],
    'energy': [],
    'loudness': [],
    'key': [], # Take majority of this, not avg
    'mode': [], # Take majority of this, not avg
    'speechiness': [],
    'acousticness': [],
    'instrumentalness': [],
    'liveness': [],
    'valence': [],
    'tempo': [],
    'duration_ms': [],
    'time_signature': [] # Take majority of this, not avg
}

weeks = []

for week in weeks_collection.find(): # Iterates over all weeks
    date = week['date']

    weeks.append(date)
    
np.set_printoptions(threshold=np.inf)

print(np.sort(weeks))

    # feature_arr = blank_feature_arrays

    # for id in week['ids']:
    #     song_object = songs_collection.find_one({'id': id})

    #     feature_arr['danceability'].append(song_object['danceability'])
    #     feature_arr['energy'].append(song_object['energy'])
    #     feature_arr['loudness'].append(song_object['loudness'])
    #     feature_arr['key'].append(song_object['key'])
    #     feature_arr['mode'].append(song_object['mode'])
    #     feature_arr['acousticness'].append(song_object['acousticness'])
    #     feature_arr['instrumentalness'].append(song_object['instrumentalness'])
    #     feature_arr['speechiness'].append(song_object['speechiness'])
    #     feature_arr['liveness'].append(song_object['liveness'])
    #     feature_arr['valence'].append(song_object['valence'])
    #     feature_arr['tempo'].append(song_object['tempo'])
    #     feature_arr['duration_ms'].append(song_object['duration_ms'])
    #     feature_arr['time_signature'].append(song_object['time_signature'])

    # week_average_obj = {
    #     'date': date,
    #     'danceability': np.mean(feature_arr['danceability']),
    #     'energy': np.mean(feature_arr['energy']),
    #     'loudness': np.mean(feature_arr['loudness']),
    #     'key': np.argmax(np.bincount(feature_arr['key'])), # Take majority of this, not avg
    #     'mode': np.argmax(np.bincount(feature_arr['mode'])), # Take majority of this, not avg
    #     'speechiness': np.mean(feature_arr['speechiness']),
    #     'acousticness': np.mean(feature_arr['acousticness']),
    #     'instrumentalness': np.mean(feature_arr['instrumentalness']),
    #     'liveness': np.mean(feature_arr['liveness']),
    #     'valence': np.mean(feature_arr['valence']),
    #     'tempo': np.mean(feature_arr['tempo']),
    #     'duration_ms': np.mean(feature_arr['duration_ms']),
    #     'time_signature': np.argmax(np.bincount(feature_arr['time_signature'])) # Take majority of this, not avg
    # }

    # print("FINAL")
    # print(week_average_obj)

