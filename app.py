from flask import Flask, render_template
from funcs import get_prcp, get_stations, get_summary_start, get_summary_start_end, get_tobs

app = Flask(__name__)

@app.route("/api/v1.0/precipitation")
def prcp():
    return get_prcp()


@app.route("/api/v1.0/stations")
def stations():
    return get_stations()


@app.route("/api/v1.0/tobs")
def tobs():
    return get_tobs()


@app.route("/api/v1.0/<start>")
def summary_start(start):
    return get_summary_start(start)


@app.route("/api/v1.0/<start>/<end>")
def summary_start_end(start, end):
    return get_summary_start_end(start, end)


@app.route("/")
def home():
    return render_template('index.html', name='home')


if __name__ == "__main__":
    app.run(debug=True)