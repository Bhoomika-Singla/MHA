# Run the following commands to start the server...
# . venv/bin/activate             Activates the virtual environment
# flask --app app.py run          Starts the server

from flask import Flask, request, jsonify
import pymongo
import numpy as np
from datetime import datetime
import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)

    return app

def get_available_dates(db):
    weeks = []
    for week in db['weeks'].find(): # Iterates over all weeks
        date = week['date']

        weeks.append(datetime.strptime(date, '%Y-%m-%d').date())

    return np.sort(weeks)

app = create_app()

# Load environment variables
load_dotenv()

client = pymongo.MongoClient(f"mongodb+srv://BigDataUser:{os.environ.get('MONGO_PASS')}@bigdatamhacluster.cu0olpo.mongodb.net/?retryWrites=true&w=majority", serverSelectionTimeoutMS=5000)
db = client['MHA'] # Accessed by `flask.current_app.db`

available_dates = get_available_dates(db) # Accessed by flask.current_app.available_dates

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
                for date in available_dates:
                    if date > start_date:
                        week_data = week_agg_collection.find_one({'date': datetime.strftime(date, '%Y-%m-%d')})
                        week_data['_id'] = ''
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

                # IMPLEMENT THIS
                return "TODO"
            elif interval == 'Year':
                year_agg_collection = db['year_aggregate_top_100']
                year_counter = 0
                year_data = []

                for year in range(start_date.year, end_date.year):
                    year_data = year_agg_collection.find_one({'year': year})
                    year_data['id'] = ''
                    year_data.append(
                        {
                            'year_number': year_counter,
                            'data': year_data
                        }
                    )
                    year_counter += 1

                return jsonify(year_data)

            else:
                raise ValueError("Invalid interval")
        except Exception as e:
            print("ERROR:", e)
            return e