"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def portfolio():
    """Return a portfolio page."""
    return render_template('bootstrap-prestructure.html')

@app.route('recitation')
def recitation():
    """
    Return the recitation application for DD1368.
    :return: Jinja2 Template
    """
    return render_template('bootstrap-recitation.html')

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
