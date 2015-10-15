
import os.path
import json
from itertools import product
from operator import itemgetter
import datetime

import requests
import dateutil.parser as dtparse
from flask import g

from sorters import sorters
from memoize import memoized

baseurl = "https://www.googleapis.com/qpxExpress/v1/trips/search"
headers = {'content-type': 'application/json'}

basedir = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../..')
keypath = os.path.join(basedir,'apikey')
apikey = open(keypath).read()
basequery = open(
	os.path.join(basedir,'slothair','templates','search_request.json')
).read()

def get_sorted(routes, sortby):
	return sorted(routes, key=sorters[sortby])

def get_routes(origin, dest, date, numresults, refundable):
	return get_multi(
		get_possibilities(
			origin,
			dest,
			date
		),
		numresults,
		refundable
	)

def get_dates(dates):
	if '+' in dates:
		start, number = dates.split('+')
		start = dtparse.parse(start).date()
		dates = [start.isoformat()]
		for i in range(int(number)):
			start += datetime.timedelta(days=1)
			dates.append(start.isoformat())
		return dates
	else:
		return dates.split(',')

def get_possibilities(origins, destinations, dates):
	return list(product(
		origins.split(','),
		destinations.split(','),
		get_dates(dates)
	))

def update_data(orig, upd):
	retval = {}
	for cat, items in orig.items():
		orig[cat] += upd[cat]
		retval[cat] = orig[cat]
	return retval

def process_data(trips, data):
	for result in trips:
		for slc in result['slice']:
			for segment in slc['segment']:
				segment["flight"]["carrier_display"] = next(
					x['name'] for x in data['carrier'] 
					if x['code'] == segment["flight"]["carrier"]
				)
	return trips

def get_multi(possibilities, numresults, refundable):
	trips, data = get_slice_trips(
		get_slice( *possibilities[0] + (numresults, refundable) )
	)
	g.qpk_lookup = data
	try:
		for p in possibilities[1:]:
			subresult, p_data = get_slice_trips(
				get_slice(*p + (numresults, refundable) )
			)
			update_data(data, p_data)
			trips += subresult
	except IndexError:
		pass
	return process_data(trips, data)

def get_slice_trips(tslice):
	try:
		return tslice['trips']['tripOption'], tslice['trips']['data']
	except KeyError:
		print tslice
		raise

def get_slice(origin, dest, date, numresults, refundable):
	params = {
		"key": apikey
	}
	query = json.loads(basequery)
	query['request']['slice'][0]['origin'] = origin
	query['request']['slice'][0]['destination'] = dest
	query['request']['slice'][0]['date'] = date
	query['request']['solutions'] = numresults
	query['request']['refundable'] = refundable
	r = requests.post(
		baseurl,
		params = params,
		data = json.dumps(query),
		headers = headers
	)
	result = json.loads(r.text)
	if 'error' in result:
		print r.text
		raise ValueError
	return result

if __name__ == '__main__':
	print get_routes('LAX,SFO', 'NRT,HKG', '2015-12-25,2015-12-26', 10)
