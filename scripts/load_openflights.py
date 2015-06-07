"""Load the 3 csv files from openflights.org into the slothair pg db."""

import os

import psycopg2

conn = psycopg2.connect(dbname='slothair')
cur = conn.cursor()

import_path = os.path.abspath('../import')
script_path = '../sql/schema.sql'

cur.execute(open(script_path).read())

for table in ('airlines', 'airports', 'routes'):
	cur.execute(
		"""COPY %s FROM '%s' (FORMAT CSV);""" % (
			table,
			os.path.join(import_path,'%s.csv' % table),
		)
	)

conn.commit()

cur.execute("""REFRESH MATERIALIZED VIEW INTERNATIONAL_ROUTES;""")
cur.execute("""REFRESH MATERIALIZED VIEW ROUTES_PER_AIRPORT;""")

conn.commit()