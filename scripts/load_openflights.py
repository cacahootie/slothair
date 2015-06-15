"""Load the 3 csv files from openflights.org into the slothair pg db."""

import os
import subprocess

import psycopg2

conn = psycopg2.connect(dbname='slothair', user='slothair')
cur = conn.cursor()

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import_path = os.path.join(basedir, 'import')
script_path = os.path.join(basedir, 'sql','schema.sql')

print script_path

subprocess.call(['psql -U slothair -d slothair -f ' + script_path], shell=True)

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
cur.execute("""REFRESH MATERIALIZED VIEW INTERNATIONAL_ROUTES_PER_AIRPORT;""")

conn.commit()
