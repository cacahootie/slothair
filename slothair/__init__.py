"""Explore flight routes."""

import os
import time

import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, render_template, redirect, request

from forms import FlightSearchForm
from interfaces.qpx import get_routes, get_sorted
from formatters import isodate_time, duration, currency_symbol
import models


basedir = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(basedir,'static','index.html')

try:
    conn = psycopg2.connect(dbname='slothair', user='slothair')
except psycopg2.OperationalError:
    time.sleep(3)
    conn = psycopg2.connect(dbname='slothair', user='slothair')

app = Flask(
    'slothair',
    static_folder=os.path.join(basedir,'static'),
    static_url_path='/static'
)

app.jinja_env.filters['isodate_time'] = isodate_time
app.jinja_env.filters['duration'] = duration
app.jinja_env.filters['currency_symbol'] = currency_symbol

@app.route("/")
def index():
    return open(index_path).read()

@app.route("/search/", methods=['GET'])
def search_get():
    return render_template('search.html', form = FlightSearchForm())

@app.route("/search/", methods=['POST'])
def search_post():
    form = FlightSearchForm(request.form)
    if form.validate():
        routes = get_routes(
            form.origin.data,
            form.dest.data,
            form.date.data,
            form.numresults.data,
            form.refundable.data
        )
        return jsonify({"results":routes})
    return redirect('/search/results/')

@app.route("/search/results/", methods=['POST'])
def search_results():
    form = FlightSearchForm(request.form)
    return render_template(
        'search_results.html',
        form = form,
        results = get_sorted( get_routes(
            form.origin.data,
            form.dest.data,
            form.date.data,
            form.numresults.data,
            form.refundable.data
        ), form.sortby.data )
    )

@app.route("/routes/<source>")
def routes(source):
    return jsonify(models.routes(source))

@app.route("/airport/<iata>")
def airport(iata):
    return jsonify(models.airport(iata))

@app.route("/sources")
def sources():
    return jsonify(models.sources())


