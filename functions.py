import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, MetaData, inspect, Table
from flask import jsonify

def init_engine():
    engine = create_engine("sqlite:///../db/hawaii.sqlite")
    Base = automap_base()
    return engine, Base


def get_prcp():
    engine, Base = init_engine()
    Base.prepare(engine, reflect=True)

    qry = engine.execute("""
        select date, sum(prcp) as prcp
        from measurement
          where date between '2016-08-23' and '2017-08-23'
          group by date
          order by date desc;
    """).fetchall()

    summary = pd.DataFrame(qry,columns=['date','data']).set_index('date').to_dict()
    return jsonify(summary)


def get_stations():
    engine, Base = init_engine()
    Base.prepare(engine, reflect=True)

    qry = engine.execute("""
        select *
        from station;
    """).fetchall()

    summary = pd.DataFrame(qry,columns=['id','station','name','latitude','longitude','elevation']).set_index('station').transpose().to_dict()
    return jsonify(summary)


def get_tobs():
    engine, Base = init_engine()
    Base.prepare(engine, reflect=True)

    obs_station = engine.execute("""
        select station
              ,count(tobs) as tobs
        from measurement
          group by station
          order by tobs desc;
    """).fetchall()

    qry = engine.execute(f"""
        select date
              ,station
              ,tobs
        from measurement
          where date between '2016-08-23' and '2017-08-23'
          group by date, station
          order by date desc;
    """).fetchall()

    summary = pd.DataFrame(qry, columns=['date','station','data'])\
        .set_index('station')\
        .loc[obs_station[0][0]]\
        .reset_index()\
        .drop(columns=['station'])\
        .set_index('date')\
        .sort_values(by=['date'], ascending=False)\
        .to_dict()

    return jsonify(summary)


def get_summary_start(start):
    engine, Base = init_engine()
    Base.prepare(engine, reflect=True)

    session = Session(engine)
    Measurement = Base.classes.measurement

    qry = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()

    summary = pd.DataFrame(qry, columns=['min','avg','max'], index=['temp']).transpose().to_dict()
    return jsonify(summary)


def get_summary_start_end(start, end):
    engine, Base = init_engine()
    Base.prepare(engine, reflect=True)

    session = Session(engine)
    Measurement = Base.classes.measurement

    qry = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    summary = pd.DataFrame(qry, columns=['min','avg','max'], index=['temp']).transpose().to_dict()
    return jsonify(summary)