# FLASK APP:

# ---------------------------------------------------------------------------------------------------------------
# Import dependencies
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

# ---------------------------------------------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------------------------------------------
    # Homepage route
@app.route("/")
def home():
    """Available routes"""
    return (
        "<b>HONOLULU, HAWAII. CLIMATE ANALYSIS:</b><br/><br/>"
        "<b>Available Routes:</b><br/><br/>"
        "Precipitation: /api/v1.0/precipitation<br/>"
        "Stations: /api/v1.0/stations<br/>"
        "TOBS Most Active Station: /api/v1.0/tobs<br/><br/>"

        "<b>Available Routes with specific dates (range from 2010-01-01 to 2017-08-23):</b><br/><br/>"
        "Start Date Only Data (YYYY-MM-DD): /api/v1.0/datesearch/<startDate><br/>"
        "Start/End Date Data (YYYY-MM-DD)/(YYYY-MM-DD): /api/v1.0/datesearch/<startDate></><endDate>"
    )

    # ---------------------------------------------------------------------------------------------------------------
    # Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Precipitation data"""
    
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

        # Return JSON
    return jsonify(preciptData)

    # ---------------------------------------------------------------------------------------------------------------
    # Stations Route
@app.route("/api/v1.0/stations")
def stations():  
    """Stations data"""

        # Query to get date an precipitation data
    query_stations = session.query(Station.station, Station.name, Station.name, Station.latitude,
                                   Station.longitude, Station.elevation).all()

        # Create dictionary in json format
    stationData = []
    for row in query_stations:
        station_dict = {}
        station_dict["station"] = row.station
        station_dict["name"] = row.name
        station_dict["latitude"] = row.latitude
        station_dict["longitude"] = row.longitude
        station_dict["elevation"] = row.elevation
        stationData.append(station_dict)

        # Return JSON
    return jsonify(stationData)

    # ---------------------------------------------------------------------------------------------------------------
    # Date and tobs of the most-active station (previous year data) Route
@app.route("/api/v1.0/tobs")
def tobs():  
    """Date and tobs most-active station data"""

        # Query to get date an precipitation data
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    sta = [Measurement.station, func.count(Measurement.station)]

    most_active_stations = session.query(*sta).\
                        group_by(Measurement.station).\
                        order_by(func.count(Measurement.station).desc()).all()
    
    most_active_station_id = most_active_stations[0][0]
    print(f'Most Active Station: {most_active_station_id}')

    tobs_last_year = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
                        filter(Measurement.date >= query_date).\
                        filter(Measurement.station == most_active_station_id).all()
    
        # Create dictionary in json format
    tobsData = []
    for row in tobs_last_year:
        tobs_dict = {}
        tobs_dict["station"] = row.station
        tobs_dict["date"] = row.date
        tobs_dict["temp"] = row.tobs
        tobsData.append(tobs_dict)

        # Return JSON
    return jsonify(tobsData)

    # ---------------------------------------------------------------------------------------------------------------
    # Start date (only) Route
@app.route("/api/v1.0/datesearch/<startDate>")
def start_only(startDate):  
    """Start date (only) data"""

        # Query to get data for the specific start date
    sel = [Measurement.date, func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)]

    results =  (session.query(*sel)
                       .filter(Measurement.date >= startDate)
                       .group_by(Measurement.date)
                       .all())
    
        # Create dictionary in json format
    dates = []                       
    for result in results:
        date_dict = {}
        date_dict["date"] = result[0]
        date_dict["max_temp"] = result[1]
        date_dict["min_temp"] = result[2]
        date_dict["avg_temp"] = result[3]
        dates.append(date_dict)
    
        # Return JSON
    return jsonify(dates)

    # ---------------------------------------------------------------------------------------------------------------
    # Start and End date Route
@app.route("/api/v1.0/datesearch/<startDate>/<endDate>")
def start_end(startDate, endDate):  
    """Start and End data"""

        # Query to get data for the specific start and end date
    sel = [Measurement.date, func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)]

    results =  (session.query(*sel)
                       .filter(Measurement.date >= startDate)
                       .filter(Measurement.date <= endDate)
                       .group_by(Measurement.date)
                       .all())
    
        # Create dictionary in json format
    dates = []                       
    for result in results:
        date_dict = {}
        date_dict["date"] = result[0]
        date_dict["max_temp"] = result[1]
        date_dict["min_temp"] = result[2]
        date_dict["avg_temp"] = result[3]
        dates.append(date_dict)
    
        # Return JSON
    return jsonify(dates)

# ---------------------------------------------------------------------------------------------------------------
# Close Session
session.close()

# Run APP
if __name__ == "__main__":
    app.run(debug=True)
