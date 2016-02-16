from datetime import datetime

from flask import (
    render_template, request, jsonify, make_response, abort, redirect, url_for,
    session)

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from dqm import app
from dqm.database import db_session
from dqm.models import DataQualityRun, DataQualitySubRun

@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return "Hello, World!"
