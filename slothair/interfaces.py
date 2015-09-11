
import os.path
import json
from itertools import product
from operator import itemgetter

import requests
import dateutil.parser as dtparse
import datetime

baseurl = "https://www.googleapis.com/qpxExpress/v1/trips/search"
headers = {'content-type': 'application/json'}

basedir = os.path.dirname(os.path.abspath(__file__))
keypath = os.path.join(basedir,'apikey')
apikey = open(keypath).read()
basequery = open(os.path.join(basedir,'templates','search_request.json')).read()

sorters = {
	'price': lambda x: float(x['saleTotal'].replace('USD','')),
}

def get_sorted(routes, sortby):
	return sorted(routes, key=sorters[sortby])

def get_routes(origin, dest, date, numresults):
	return get_multi( get_possibilities(origin, dest, date), numresults )

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
		retval[cat] = [
			json.loads(x) for x in set(
				[ json.dumps(y, sort_keys=True) for y in items + upd[cat] ]
			)
		]
	return retval

def get_multi(possibilities, numresults):
	retval = get_slice_trips( get_slice( *possibilities[0] + (numresults,) ) )
	try:
		for p in possibilities[1:]:
			subresult = get_slice_trips( get_slice(*p + (numresults,) ) )
			retval += subresult
	except IndexError:
		pass
	return retval

def get_slice_trips(tslice):
	return tslice['trips']['tripOption']
	try:
		return {
			"results":tslice['trips']['tripOption'],
			"data":tslice['trips']['data']
		}
	except KeyError:
		print tslice
		raise

def get_slice(origin, dest, date, numresults):
	params = {
		"key": apikey
	}
	query = json.loads(basequery)
	query['request']['slice'][0]['origin'] = origin
	query['request']['slice'][0]['destination'] = dest
	query['request']['slice'][0]['date'] = date
	query['request']['solutions'] = numresults
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
