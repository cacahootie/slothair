"""Explore flight routes."""

import os
import time
import urllib

import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, render_template, redirect, request

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

def get_routes_sorted():
    return get_sorted( get_routes(
            request.args.get('origin'),
            request.args.get('destination'),
            request.args.get('departure'),
            request.args.get('numresults'),
            request.args.get('refundable')
        ), request.args.get('sortby')
    )

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

@app.route("/forms/sourcelist")
def sourcelist_props():
    return jsonify({
        "type": "string",
        "enum": models.sourcelist()["results"]
    })
