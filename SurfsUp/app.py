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
    return   












# Instance for Flask
app = Flask(__name__)

# Start at the home page
@app.route("/")
def home():
    print('Server received request for Home Page')
    return ('Welcome to home page')
