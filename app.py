import numpy as np
import datetime as dt
import requests
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, request


# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station




# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    print("List all available api routes.")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/stations_route<br/>"
        f"/api/v1.0/precipitation_route<br/>"
        f"/api/v1.0/tobs_route<br/>"
        f"/api/v1.0/start_route/<some_date><br/>"
        f"/api/v1.0/start_end_route/dates"
    )


@app.route("/api/v1.0/stations_route")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    print("Return a list of all stations")
    # Query all stations
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station, name, latitude, longitude, elevation in results:
        stations_dict = {}
        stations_dict["station"] = station
        stations_dict["name"] = name
        stations_dict["laltitude"] = latitude
        stations_dict["longitude"] = longitude
        stations_dict["elevation"] = elevation
        all_stations.append(stations_dict)

    return jsonify(all_stations)



@app.route("/api/v1.0/precipitation_route")
def measurements():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    print("Return a list of  data and precipitation scores")
    # Set begindate the date 1 year ago from the last data point in the database
    begindate = dt.datetime(2016, 8, 23)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= begindate).\
        order_by(Measurement.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_measurements
    all_measurements = []
    for date, prcp in results:
        measurements_dict = {}
        measurements_dict[date] = prcp
        #measurements_dict["prcp"] = prcp
        all_measurements.append(measurements_dict)

    return jsonify(all_measurements)




@app.route("/api/v1.0/tobs_route")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    print("Return a list of TOBS data")
    
    # Set begindate the date 1 year ago from the last data point in the database
    begindate = dt.datetime(2016, 8, 23)

    # Query the last 12 months of temperature observation data for this station and plot the results as a histogram
    results = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.station=='USC00519281').\
            filter(Measurement.date >= begindate).\
            order_by(Measurement.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_measurements
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)



@app.route("/api/v1.0/start_route/<some_date>", methods=['GET'])
def start(some_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    print("Using the Date from the URL, return min, max and Avg Temps")
    selected_date = dt.datetime.strptime(some_date, "%Y-%m-%d").date()
    results = session.query(func.Min(Measurement.tobs), func.Max(Measurement.tobs), func.Avg(Measurement.tobs)).\
                        filter(Measurement.date>=selected_date).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of all_stats
    all_stats = []
    for min, max, avg in results:
        stats_dict = {}
        stats_dict["min"] = min
        stats_dict["max"] = max
        stats_dict["avg"] = avg
        all_stats.append(stats_dict)

    return jsonify(all_stats)



@app.route("/api/v1.0/start_end_route/dates", methods=['GET'])
def start_end():
    start_date  = request.args.get('start_date', None)
    end_date  = request.args.get('end_date', None)
    # Create our session (link) from Python to the DB
    session = Session(engine)

    print("Using the Date from the URL, return min, max and Avg Temps")
    s_date = dt.datetime.strptime(start_date, "%Y-%m-%d").date()
    e_date = dt.datetime.strptime(end_date, "%Y-%m-%d").date()
    results = session.query(func.Min(Measurement.tobs), func.Max(Measurement.tobs), func.Avg(Measurement.tobs)).\
                         filter(Measurement.date<=e_date).\
                        filter(Measurement.date>=s_date).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of all_stats
    all_stats2 = []
    for min, max, avg in results:
        stats_dict2 = {}
        stats_dict2["min"] = min
        stats_dict2["max"] = max
        stats_dict2["avg"] = avg
        all_stats2.append(stats_dict2)

    return jsonify(all_stats2)


if __name__ == '__main__':
    app.run(debug=True)
