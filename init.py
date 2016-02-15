import sys
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from dqm.database import init_db, db_session
from dqm.models import DataQualitySubRun, DataQualityRun

init_db()
