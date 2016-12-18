from sqlalchemy import event
from sqlalchemy.schema import CreateSchema
#from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

from dqm import app

db = SQLAlchemy(app)

db_session = db.session

Base = db.Model

def init_db():
    import dqm.models

    # create database schema
    # see http://stackoverflow.com/questions/13677781/getting-sqlalchemy-to-issue-create-schema-on-create-all
    event.listen(Base.metadata, 'before_create', CreateSchema('dqm'))

    # create database tables
    db.create_all()

#from sqlalchemy import create_engine
#from sqlalchemy.orm import scoped_session, sessionmaker
#from sqlalchemy.ext.declarative import declarative_base
#
#engine = create_engine('postgresql://localhost/lariat_dqm', echo=False)
#
#db_session = scoped_session(
#    sessionmaker(autocommit=False, autoflush=False, bind=engine)
#    )
#
#Base = declarative_base()
#Base.query = db_session.query_property()
#
#def init_db():
#    import lariat_dqm.models
#    Base.metadata.create_all(bind=engine)
