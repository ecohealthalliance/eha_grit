import flask

application = flask.Flask(__name__)
application.config.from_object('config')

import bratwurst.views
