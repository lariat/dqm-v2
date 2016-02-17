from datetime import datetime

from flask import (
    render_template, request, jsonify, make_response, abort, redirect, url_for,
    session)

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from dqm import app
from dqm.database import db_session
from dqm.models import DataQualityRun, DataQualitySubRun, DataQualityLatest

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

def fetch():
    """ Fetch Run or SubRun from database. """

    r = request.args.get('run', None)
    sr = request.args.get('subrun', None)

    run, subrun = 0, 0

    if not r and not sr:
        return "Hello, World!"

    if not r and sr:
        return "Run number not specified!"

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

    if r and not sr:
        Run = fetch_run(run)
        if isinstance(Run, DataQualityRun):
            print Run.date_time_updated
        return "Run: {}".format(run)
        return Run

    if r and sr:
        SubRun = fetch_subrun(run, subrun)
        if isinstance(SubRun, DataQualitySubRun):
            print SubRun.date_time
        return "Run: {}; sub-run: {}".format(run, subrun)
        return SubRun

@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/q')
def q():
    return fetch()

#@app.route('/test')
#def test():
#    q = request.args.get('q', None)
#    q = str(q)
#    return q
