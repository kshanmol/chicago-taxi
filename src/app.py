from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from helpers import load_parquet, group_by_date
from helpers import total_trips, average_speed_24hrs

import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

data = load_parquet("/tmp/chicago_taxi_trips_2020.parquet")
print(data.info())
grouped_data = group_by_date(data)

@app.route('/total_trips', methods=['GET'])
def get_trips():
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    return json.dumps(total_trips(start_date, end_date, grouped_data))

@app.route('/average_speed_24hrs', methods=['GET'])
def get_average_speed_24hrs():
    date = request.args.get('date')
    return json.dumps(average_speed_24hrs(date, grouped_data))

@app.route('/', methods=['GET'])
def index():
    return "Hello, world"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)