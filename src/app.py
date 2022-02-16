from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

from helpers import load_parquet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

data = load_parquet("/tmp/chicago_taxi_trips_2020.parquet")
print(data.info())

@app.route('/', methods=['GET'])
def index():
    return "Hello, world"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)