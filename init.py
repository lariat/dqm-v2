import sys
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from dqm.database import init_db, db_session
from dqm.models import DataQualitySubRun, DataQualityRun, DataQualityLatest

init_db()

latest = DataQualityLatest(0, 0, datetime.now())

db_session.add(latest)

try:
    db_session.commit()
except IntegrityError as e:
    db_session.rollback()
    print str(e)
except SQLAlchemyError as e:
    db_session.rollback()
    print str(e)

db_session.remove()
