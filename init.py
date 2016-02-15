import sys
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from dqm.database import init_db, db_session
from dqm.models import DataQualitySubRun, DataQualityRun

init_db()

"""
subrun = DataQualitySubRun(
    run=1,
    subrun=1,
    date_time=datetime.strptime('2015-06-17 02:16 PM', '%Y-%m-%d %I:%M %p'),
    date_time_added=datetime.now(),
    )

#run = DataQualityRun(
#    run=1,
#    date_time=datetime.strptime('2015-06-17 02:16 PM', '%Y-%m-%d %I:%M %p'),
#    date_time_added=datetime.now(),
#    )

# subrun
subrun.mwpc_data_blocks = 10
#subrun.caen_data_blocks = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
subrun.caen_data_blocks = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
    None, None, None, None, None, None, None,
    None, None, None, None, None, None, None,
    24,
    ]
#subrun.caen_data_blocks = {
#    0:1, 1:2, 2:3, 3:4, 4:5, 5:6, 6:7, 7:8, 8:9, 9:10, 24:25 }
#subrun.caen_data_blocks = {
#    str(key):str(value) for key, value in subrun.caen_data_blocks.items() }
subrun.caen_board_08_adc_histogram = [
    [ 0, 1 ],
    [ 2, 3 ],
    ]

db_session.add(subrun)

try:
    db_session.commit()
except IntegrityError as e:
    db_session.rollback()
    print str(e)
except SQLAlchemyError as e:
    db_session.rollback()
    print str(e)

db_session.remove()
"""

