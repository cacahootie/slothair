"""Explore flight routes."""

import os
import time

import psycopg2
import psycopg2.extras
from flask import Flask, jsonify

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

@app.route("/")
def index():
    return open(index_path).read()

@app.route("/routes/<source>")
def routes(source):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("""
    		SELECT distinct(dest_iata), airports.* FROM ROUTES
    		JOIN AIRPORTS
    			ON routes.dest_id = airports.airport_id
    		WHERE 
    			source_id = (
    				SELECT airport_id FROM AIRPORTS
    				WHERE iata_faa_id = %(source_iata)s
    			)
    		;""",
    		{
    			'source_iata': source
    		}
    	)
    	destinations = [dict(r) for r in cur]
    	return jsonify({
    		'results':destinations,
    		'source_id': source,
    		'numresults': len(destinations)
    	})

@app.route("/airport/<iata>")
def airport(iata):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("""
            SELECT * FROM AIRPORTS
            WHERE IATA_FAA_ID = %(iata)s
            ;""",
            {
                'iata': iata
            }
        )
        return jsonify([dict(r) for r in cur][0])

@app.route("/sources")
def sources():
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("""
            SELECT NUM_ROUTES, AIRPORTS.* FROM ROUTES_PER_AIRPORT
            JOIN AIRPORTS
                ON ROUTES_PER_AIRPORT.source_id = AIRPORTS.airport_id
            WHERE NUM_ROUTES > 5
            ;"""
        )
        sources = [dict(r) for r in cur]
        return jsonify({
            'results':sources,
            'numresults': len(sources)
        })


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8008,
        debug=True
    )
