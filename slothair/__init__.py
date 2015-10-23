"""Explore flight routes."""

import os
import time
import urllib

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

def get_routes_sorted():
    return get_sorted( get_routes(
            request.args.get('origin'),
            request.args.get('destination'),
            request.args.get('departure'),
            request.args.get('numresults'),
            request.args.get('refundable')
        ), request.args.get('sortby')
    )

@app.route("/search/", methods=['POST'])
def search_post():
    form = FlightSearchForm(request.form)
    if form.validate():
        return redirect('/search/results/?' + urllib.urlencode({
            "origin": form.origin.data,
            "destination": form.dest.data,
            "departure": form.date.data,
            "numresults": form.numresults.data,
            "refundable": form.refundable.data,
            "sortby": form.sortby.data,
            "result_format": form.result_format.data
        }))

@app.route("/search/results/", methods=['GET'])
def search_results():
    if request.args.get('result_format') == 'html':
        return render_template(
            'search_results.html',
            results = get_routes_sorted()
        )
    elif request.args.get('result_format') == 'json':
        return jsonify({"results":get_routes_sorted()})

@app.route("/routes/<source>")
def routes(source):
    return jsonify(models.routes(source))

@app.route("/airport/<iata>")
def airport(iata):
    return jsonify(models.airport(iata))

@app.route("/sources")
def sources():
    return jsonify(models.sources())

@app.route("/sourcelist")
def sourcelist():
    return jsonify(models.sourcelist())

@app.route("/forms/sourcelist")
def sourcelist_props():
    return jsonify({
        "type": "string",
        "enum": models.sourcelist()["results"]
    })
