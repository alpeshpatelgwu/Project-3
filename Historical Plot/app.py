# import necessary libraries
from sqlalchemy import (func, create_engine)
import pymysql
pymysql.install_as_MySQLdb()

import pandas as pd

from flask import (
    Flask,
    render_template,
    jsonify)

from flask_sqlalchemy import SQLAlchemy
from flask.json import JSONEncoder
from datetime import date

remote_db_endpoint = 'gwcodingbootcamp.cr0gccbv4ylw.us-east-2.rds.amazonaws.com'
remote_db_port = '3306'
remote_gwsis_dbname = 'bikeshare_db'
remote_gwsis_dbuser = 'root'
remote_gwsis_dbpwd = 'braddocks'

# AWS Database Connection
engine = create_engine(f"mysql://{remote_gwsis_dbuser}:{remote_gwsis_dbpwd}@{remote_db_endpoint}:{remote_db_port}/{remote_gwsis_dbname}")
# Create a remote database engine connection
conn = engine.connect()

class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

# Create a route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

# Query the database and return the jsonified results
@app.route("/data")
def data():
    conn = engine.connect()

    #bike_df = pd.read_sql("SELECT * FROM bikeshare WHERE time = '2019-04-06 09:52:00'", conn)
    bike_df = pd.read_sql("SELECT * FROM bikeshare WHERE term_id = 1", conn)
    #time = [result.time for result in results]
    #num_bikes = [result.num_bikes for result in results]

    #trace = {
    #  "type": "scatter",
    #  "x": time,
    #  "y": num_bikes
    #}

    #return jsonify(trace)
    return jsonify(bike_df.to_dict(orient="records"))

    #bike_json = bike_df.to_json(orient="records")
    #return bike_json

if __name__ == "__main__":
    app.run(debug=True)
