import os

from flask import Flask

from formatters import isodate_time, duration, currency_symbol

basedir = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(basedir,'static','index.html')

app = Flask(
    'slothair',
    static_folder=os.path.join(basedir,'static'),
    static_url_path='/static'
)

app.jinja_env.filters['isodate_time'] = isodate_time
app.jinja_env.filters['duration'] = duration
app.jinja_env.filters['currency_symbol'] = currency_symbol

import views
