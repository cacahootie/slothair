"""Load the 3 csv files from openflights.org into the slothair pg db."""

import os

import psycopg2

conn = psycopg2.connect(dbname='slothair')
cur = conn.cursor()

import_path = os.path.abspath('../import')
for table in ('airlines', 'airports', 'routes'):
	cur.execute(
		"""COPY %s FROM '%s' (FORMAT CSV);""" % (
			table,
			os.path.join(import_path,'%s.csv' % table),
		)
	)

conn.commit()