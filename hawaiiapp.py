import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>tobs</a><br/>"
        f"<a href='/api/v1.0/<start>'>start date</a><br/>"
        f"<a href='/api/v1.0/<start>/<end>'>start and end date</a><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    #Convert the query results to a dictionary using date as the key and prcp as the value
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    session.close()

    #create the dictionary
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    ##Return List of Stations in JSON
    results = session.query(Station.name, Station.station).group_by(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_results = list(np.ravel(results))

    return jsonify(all_results)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    ##return the list of temperature obeservations of the most active station for the last year
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23', Measurement.station == 'USC00519281').order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    all_results = list(np.ravel(results))

    return jsonify(all_results)

@app.route("/api/v1.0/<start>")
def start():
    session = Session(engine)

    ##Analysis goes here

@app.route("/api/v1.0/<start>/<end>")
def startend():
    session = Session(engine)

    ##Analysis goes here


if __name__ == '__main__':
    app.run(debug=True)