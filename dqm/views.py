from datetime import datetime, timedelta

import numpy as np

from flask import (
    render_template, request, jsonify, make_response, abort, redirect, url_for,
    session)

from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from redis import Redis

from dqm import app
from dqm.database import db_session
from dqm.models import DataQualityRun, DataQualitySubRun, DataQualityLatest
import dqm.allowed as allowed

from classes import Histogram
from metrics.binning import round_time, date_time_bins

# redis client instance
redis = Redis()

def fetch_subrun(run, subrun):
    """ Fetch SubRun from database. """
    try:
        SubRun = DataQualitySubRun.query.filter_by(run=run, subrun=subrun).one()
        return SubRun
    except:
        return None
    return None

def fetch_run(run):
    """ Fetch Run from database. """
    try:
        Run = DataQualityRun.query.filter_by(run=run).one()
        return Run
    except:
        return None
    return None

def latest_run_subrun():
    """ Get the latest run and sub-run numbers. """
    Latest = DataQualityLatest.query.order_by(
        DataQualityLatest.date_time_updated.desc()).first()
    run = Latest.run
    subrun = Latest.subrun
    date_time = Latest.date_time_updated
    return run, subrun

def check_run_subrun(r, sr):
    """ Check to see if the run and sub-run numbers are OK. """

    run, subrun = None, None

    if (not r and not sr) or (not r and sr):
        print "Run number not specified!"
        return run, subrun

    if r == "latest" or sr == "latest":
        latest_run, latest_subrun = latest_run_subrun()

    if r:
        if r == "latest":
            run = latest_run
        else:
            try:
                run = int(r)
            except:
                run = None

    if sr:
        if sr == "latest":
            subrun = latest_subrun
        else:
            try:
                subrun = int(sr)
            except:
                subrun = None

    return run, subrun

@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    return render_template('home.html', title="Home")

@app.route('/json')
def json():

    # /json?query=caen_board_0_data_blocks&run=latest&subrun=3

    run = request.args.get('run', None)
    subrun = request.args.get('subrun', None)
    query = request.args.get('query', None)

    run, subrun = check_run_subrun(run, subrun)
    db_row_object = None

    if run and subrun:
        db_row_object = fetch_subrun(run, subrun)
    elif run and not subrun:
        db_row_object = fetch_run(run)

    if not db_row_object or not query:
        return "NULL"

    db_row_object_dict = dict(db_row_object.__dict__) 
    db_row_object_dict.pop('_sa_instance_state', None)

    query = str(query)
    parameter_list = query.split(' ')

    # check to see if the parameters exists
    for parameter in parameter_list:
        if parameter not in db_row_object_dict:
            return "NULL"

    json_data = {}
    
    for parameter in parameter_list:
        json_data[parameter] = db_row_object_dict[parameter]

    return jsonify(json_data)

@app.route('/json/latest-runs')
def json_latest_runs():
    """
        Get the last N run numbers from the database.

            limit: Limit on the number of results returned.
                   Default 100.
    """

    limit = request.args.get('limit', None)

    if not limit:
        limit = 100

    # query PostgreSQL database for the lastest runs
    db_query = db_session.query(DataQualityRun) \
        .order_by(DataQualityRun.date_time.desc())
    results = db_query.limit(limit)

    json_results = []

    for result in results:
        json_results.append({
            'run'     : result.run,
            'subruns' : result.subruns,
            })

    return jsonify(results=json_results)

@app.route('/histograms')
def histograms():

    # /histograms?query=caen_board_0_timestamps+caen_board_1_timestamps&run=latest&subrun=3

    run = request.args.get('run', None)
    subrun = request.args.get('subrun', None)
    run, subrun = check_run_subrun(run, subrun)

    db_row_object = None

    if run and subrun:
        db_row_object = fetch_subrun(run, subrun)
    elif run and not subrun:
        db_row_object = fetch_run(run)

    if not db_row_object:
        return "NULL"

    # get list of parameters from Run or SubRun
    db_row_object_dict = dict(db_row_object.__dict__) 
    db_row_object_dict.pop('_sa_instance_state', None)
    parameters = [
        s for s in db_row_object_dict if '_histogram' in s ]

    query = str(request.args.get('query', None))
    parameter_list = query.split(' ')

    # check to see if the histogram exists
    for parameter in parameter_list:
        if not any(parameter in s for s in parameters):
            return "NULL"

    json_data = {}

    # fill json_data with histogram data
    for parameter in parameter_list:
        histogram = Histogram(parameter)
        histogram.db_to_histogram(
             getattr(db_row_object, parameter + "_histogram_bin_indices"),
             getattr(db_row_object, parameter + "_histogram_counts"),
             getattr(db_row_object, parameter + "_histogram_bin_width"),
             getattr(db_row_object, parameter + "_histogram_number_bins"),
             getattr(db_row_object, parameter + "_histogram_min_bin"),
             getattr(db_row_object, parameter + "_histogram_max_bin"))
        json_data[parameter] = {
            'bins'        : histogram.bins.tolist(),
            'counts'      : histogram.counts.tolist(),
            'bin_width'   : histogram.bin_width,
            'number_bins' : histogram.number_bins,
            'min_bin'     : histogram.min_bin,
            'max_bin'     : histogram.max_bin,
            }

    return jsonify(json_data)

@app.route('/metric')
def metric():

    parameter = request.args.get('parameter', None)

    key_prefix = 'dqm/metric/1min/'
    key = key_prefix + parameter

    if redis.exists(key):
        values = redis.lrange(key, 0, -1)
        return jsonify(values=values)

    else:
        return "NULL"

@app.route('/metrics')
def metrics():
    return render_template('metrics.html',
                           title="Metrics")

@app.route('/metrics/data-stream')
def metrics_data_stream():
    return render_template('metrics-data-stream.html',
                           title="Data stream metrics")

@app.route('/metrics/tpc-pedestal-mean-deviations/induction')
def metrics_tpc_pedestal_mean_deviations_induction():
    return render_template(
        'metrics-tpc-pedestal-mean-deviations-induction.html',
        title="TPC pedestal mean deviations on induction plane")

@app.route('/metrics/tpc-pedestal-mean-deviations/collection')
def metrics_tpc_pedestal_mean_deviations_collection():
    return render_template(
        'metrics-tpc-pedestal-mean-deviations-collection.html',
        title="TPC pedestal mean deviations on collection plane")

@app.route('/metrics/tpc-pedestal-rms/induction')
def metrics_tpc_pedestal_rms_induction():
    return render_template(
        'metrics-tpc-pedestal-rms-induction.html',
        title="TPC pedestal RMS on induction plane")

@app.route('/metrics/tpc-pedestal-rms/collection')
def metrics_tpc_pedestal_rms_collection():
    return render_template(
        'metrics-tpc-pedestal-rms-collection.html',
        title="TPC pedestal RMS on collection plane")

@app.route('/data-stream')
def data_stream():

    run = request.args.get('run', "latest")
    subrun = request.args.get('subrun', None)

    live = request.args.get('live', False)

    if live == u'':
        run = "latest"
        subrun = None

    run, subrun = check_run_subrun(run, subrun)

    return render_template('data-stream.html',
                           title="Data stream",
                           run=run,
                           subrun=subrun)

@app.route('/tpc')
def tpc():

    run = request.args.get('run', "latest")
    subrun = request.args.get('subrun', None)

    live = request.args.get('live', False)

    if live == u'':
        run = "latest"
        subrun = None

    run, subrun = check_run_subrun(run, subrun)

    return render_template('tpc.html',
                           title="TPC",
                           run=run,
                           subrun=subrun)

@app.route('/caen-boards')
def caen_boards():

    run = request.args.get('run', "latest")
    subrun = request.args.get('subrun', None)

    live = request.args.get('live', False)

    if live == u'':
        run = "latest"
        subrun = None

    run, subrun = check_run_subrun(run, subrun)

    return render_template('caen-boards.html',
                           title="CAEN boards",
                           run=run,
                           subrun=subrun)

@app.route('/multi-wire-chambers')
def multi_wire_chambers():

    run = request.args.get('run', "latest")
    subrun = request.args.get('subrun', None)

    live = request.args.get('live', False)

    if live == u'':
        run = "latest"
        subrun = None

    run, subrun = check_run_subrun(run, subrun)

    return render_template('multi-wire-chambers.html',
                           title="Multi-wire chambers",
                           run=run,
                           subrun=subrun)

@app.route('/multi-wire-chambers/channels')
def multi_wire_chambers_channels():

    run = request.args.get('run', "latest")
    subrun = request.args.get('subrun', None)

    live = request.args.get('live', False)

    if live == u'':
        run = "latest"
        subrun = None

    run, subrun = check_run_subrun(run, subrun)

    return render_template('multi-wire-chambers-channels.html',
                           title="Multi-wire chambers &mdash; Channels",
                           run=run,
                           subrun=subrun)

@app.route('/multi-wire-chambers/timing')
def multi_wire_chambers_timing():

    run = request.args.get('run', "latest")
    subrun = request.args.get('subrun', None)

    live = request.args.get('live', False)

    if live == u'':
        run = "latest"
        subrun = None

    run, subrun = check_run_subrun(run, subrun)

    return render_template('multi-wire-chambers-timing.html',
                           title="Multi-wire chambers &mdash; Timing",
                           run=run,
                           subrun=subrun)

@app.route('/physics')
def physics():

    run = request.args.get('run', "latest")
    subrun = request.args.get('subrun', None)

    live = request.args.get('live', False)

    if live == u'':
        run = "latest"
        subrun = None

    run, subrun = check_run_subrun(run, subrun)

    return render_template('physics.html',
                           title='Physics',
                           run=run,
                           subrun=subrun)

