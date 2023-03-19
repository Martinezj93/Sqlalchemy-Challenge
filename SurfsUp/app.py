# FLASK APP:

# Import dependencies
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

# Data base setup
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with = engine)

# Create the classes
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask setup
app = Flask(__name__)

    # Homepage route
@app.route("/")
def home():
    """Available routes"""
    return (
        "Available Routes:<br/><br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/start<br/>"
        "/api/v1.0/start/end"
    )

    # Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Precipitation data of the last 12 months (from 2016-08-23 to 2017-08-23)"""
    
        # Query to get date an precipitation data
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prcp_scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).order_by(Measurement.date).all()

        # Create dictionary in json format
    preciptData = []
    for row in prcp_scores:
        prcp_dict = {}
        prcp_dict["date"] = row.date
        prcp_dict["prcp"] = row.prcp
        preciptData.append(prcp_dict)

    return jsonify(preciptData)

    # Stations Route
@app.route("/api/v1.0/stations")
def stations():  
    """Stations data"""
    query_stations = session.query(Station.name).all()
    stations = list(np.ravel(query_stations))

    return jsonify(stations)

if __name__ == "__main__":
    app.run(debug=True)












# Instance for Flask
app = Flask(__name__)

# Start at the home page
@app.route("/")
def home():
    print('Server received request for Home Page')
    return ('Welcome to home page')
