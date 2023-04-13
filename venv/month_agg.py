import pymongo
import numpy as np
from datetime import datetime
import os
from dotenv import load_dotenv


def connect_db():
    load_dotenv()
    client = pymongo.MongoClient(f"mongodb+srv://BigDataUser:{os.environ.get('MONGO_PASS')}@bigdatamhacluster.cu0olpo.mongodb.net/?retryWrites=true&w=majority", serverSelectionTimeoutMS=5000)
    return client['MHA'] # Accessed by `flask.current_app.db`

db = connect_db()

week_agg_collection = db['week_aggregate_top_100']
month_agg_collection = db['month_aggregate_top_100']
year_agg_collection = db['year_aggregate_top_100']

month_year_dic = {}
year_dic = {}

for week in week_agg_collection.find(): # Iterate over all week aggregates
    date = week['date']
    date_object = datetime.strptime(date, "%Y-%m-%d")

    year = date_object.year
    month = date_object.month

    month_year_tuple = (month, year)

    month_year_dic.setdefault(month_year_tuple, []).append(week)
    year_dic.setdefault(year, []).append(week)

month_aggregate = []

# # Aggregate month
for month_year in month_year_dic.keys(): # Iterate over keys
    values_arr = month_year_dic[month_year] # Arr with all objects in that month
    month = month_year[0]
    year = month_year[1]

    def_values_obj = {
        'danceability':[],
        'energy':[],
        'loudness':[],
        'speechiness':[],
        'acousticness':[],
        'instrumentalness':[],
        'liveness':[],
        'valence':[],
        'tempo':[],
        'duration_ms':[],
        'key':[],
        'mode':[],
        'time_signature':[]
    }

    for i in values_arr: # Iterate over objects in specific month_year
        for key in i.keys(): # Iterate over keys in obj
            if key != 'date' and key != '_id' and key != 'year' and key != 'month' and key != 'day':
                def_values_obj[key].append(i[key])

    month_value = {
        'month': month,
        'year': year
    }

    for key in def_values_obj.keys():
        if key == 'mode' or key == 'time_signature' or key == 'key':
            month_value[key] = int(np.bincount(def_values_obj[key]).argmax()) # Find most repeated value
        else:
            month_value[key] = float(np.mean(def_values_obj[key])) # Average other values

    month_aggregate.append(month_value)
    # Add month_value to DB here to correct collection
    month_agg_collection.insert_one(month_value)

print('Finished adding month...')
# for i in month_aggregate:
#     print(i['month'], i['year'])

year_aggregate = []

# Aggregate year
for year in year_dic.keys():
    def_values_obj = {
        'danceability':[],
        'energy':[],
        'loudness':[],
        'speechiness':[],
        'acousticness':[],
        'instrumentalness':[],
        'liveness':[],
        'valence':[],
        'tempo':[],
        'duration_ms':[],
        'key':[],
        'mode':[],
        'time_signature':[]
    }

    # year_dic[year] contains a list with all of the weeks in that year
    for obj in year_dic[year]:
        for key in obj.keys():
            if key != 'date' and key != '_id' and key != 'year' and key != 'month' and key != 'day':
                def_values_obj[key].append(obj[key])

    year_value = {
        'year': year
    }

    for key in def_values_obj.keys():
        if key == 'mode' or key == 'time_signature' or key == 'key':
            year_value[key] = int(np.bincount(def_values_obj[key]).argmax()) # Find most repeated value
        else:
            year_value[key] = float(np.mean(def_values_obj[key])) # Average other values

    year_aggregate.append(year_value)
    # Add year_value here to db
    year_agg_collection.insert_one(year_value)

print('Finished adding year...')
# for i in year_aggregate:
#     print(i['year'])