from flask import Flask

# see http://flask.pocoo.org/docs/patterns/packages/
app = Flask(__name__)

app.config.from_pyfile("config.py")

if not app.debug:
    # see http://flask.pocoo.org/docs/errorhandling/
    import logging
    app.logger.addHandler(logging.StreamHandler())

from dqm import views
