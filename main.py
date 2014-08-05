"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
import flask
app = flask.Flask(__name__)

# ============================ #
# todo(jondb) move this to its own file == #
import datetime
import babel.dates
def relative_time(dt):
    now = datetime.datetime.utcnow()
    delta = now - dt
    return babel.dates.format_timedelta(delta, locale='en_US')
# ============================ #
app.jinja_env.filters['relative_time'] = relative_time

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

import model

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return flask.render_template('index.html', name="Name")


@app.route('/log/<name>/<status>')
def log_status(name, status):
    """Return a friendly HTTP greeting."""
    error_text = flask.request.args.get('error_text', None)
    status = int(status)
    m = model.Status.update_status(name, status, error_text)
    return 'OK'


@app.route('/gocron')
def run_cron():
    import tester
    tester.run_tests()
    return 'OK'


@app.route('/report')
def report():
    data = model.Status.summary()
    return flask.render_template('report.html', data=data)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def page_not_found(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
