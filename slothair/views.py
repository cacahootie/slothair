
import os

from flask import Flask, jsonify, render_template, request

from app import app
import models
from interfaces.qpx import get_sorted, get_routes, get_origin_trips

basedir = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(basedir,'static','index.html')

@app.route("/")
def index():
    return open(index_path).read()

def get_routes_sorted():
    return get_sorted( get_routes(
            request.args.get('origin'),
            request.args.get('destination'),
            request.args.get('departure'),
            request.args.get('return_'),
            request.args.get('numresults'),
            request.args.get('refundable'),
            request.args.get('booking_class'),
        ), request.args.get('sortby')
    )

def get_origin_routes_sorted():
    return get_sorted(
        get_origin_trips(
            request.args.get('origin'),
            request.args.get('departure'),
            request.args.get('return_'),
        ),
    'price')

@app.route("/search/results/", methods=['GET'])
def search_results():
    if request.args.get('result_format') == 'html':
        return render_template(
            'search_results.html',
            results = get_routes_sorted()
        )
    elif request.args.get('result_format') == 'json':
        return jsonify({"results":get_routes_sorted()})

@app.route("/search/origin/", methods=['GET'])
def origin_results():
    return render_template(
        'search_results.html',
        results = get_origin_routes_sorted()
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

@app.route("/mostlinked/<origin>/")
def mostlinked(origin):
    return jsonify(models.mostlinked(origin))

@app.route("/forms/sourcelist")
def sourcelist_props():
    return jsonify({
        "type": "string",
        "enum": models.sourcelist()["results"]
    })
