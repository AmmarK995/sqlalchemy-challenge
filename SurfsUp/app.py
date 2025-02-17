# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)
# reflect the tables


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################

# Initialize Flask app
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
# Define the homepage route
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

# Define the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create a session (link) from Python to the database
    session = Session(engine)

    # Find the most recent date in the dataset
    latest_date = session.query(func.max(Measurement.date)).scalar()
    latest_date = dt.datetime.strptime(latest_date, "%Y-%m-%d")

    # Calculate the date one year ago from the most recent date
    one_year_ago = latest_date - dt.timedelta(days=365)

    # Query for the last 12 months of precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()

    # Close the session
    session.close()

    # Convert results to a dictionary with date as key and prcp as value
    precip_dict = {date: prcp for date, prcp in results}

    # Return JSON representation
    return jsonify(precip_dict)

# Defining the stations route
@app.route("/api/v1.0/stations")
def stations():
    # Create a session (link) from Python to the database
    session = Session(engine)

    # Query all station IDs
    results = session.query(Station.station).all()

    # Close the session
    session.close()

    # Convert list of tuples into a normal list
    stations_list = [station[0] for station in results]

    # Return JSON response
    return jsonify(stations_list)

# Defining the tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    # Create a session (link) from Python to the database
    session = Session(engine)

    # Find the most active station (station with most observations)
    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).\
        first()[0]

    # Find the most recent date in the dataset
    latest_date = session.query(func.max(Measurement.date)).scalar()
    latest_date = dt.datetime.strptime(latest_date, "%Y-%m-%d")
    one_year_ago = latest_date - dt.timedelta(days=365)

    # Query temperature observations (tobs) for the most active station in the last 12 months
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_ago).all()

    # Close the session
    session.close()

    # Convert query results into a list of dictionaries
    tobs_list = [{date: temp} for date, temp in results]

    # Return JSON response
    return jsonify(tobs_list)

# Defining the start/end routes
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats(start, end=None):
    # Create a session
    session = Session(engine)

    # Define the base query
    sel = [
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ]

    # If only start date is provided
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
    else:
        # If both start and end dates are provided
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()

    # Close the session
    session.close()

    # Extract results and format JSON response
    temp_dict = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    return jsonify(temp_dict)


# Run the app
if __name__ == "__main__":
    app.run(debug=True)