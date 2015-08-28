
import os.path
import json
from itertools import product

import requests

baseurl = "https://www.googleapis.com/qpxExpress/v1/trips/search"
headers = {'content-type': 'application/json'}

basedir = os.path.dirname(os.path.abspath(__file__))
keypath = os.path.join(basedir,'apikey')
apikey = open(keypath).read()
basequery = open(os.path.join(basedir,'templates','search_request.json')).read()

def get_routes(origin, dest, date):
	return get_multi(get_possibilities(origin, dest, date))

def get_possibilities(origins, destinations, dates):
	return list(product(
		origins.split(','),
		destinations.split(','),
		dates.split(',')
	))

def get_multi(possibilities):
	retval = get_slice_trips(get_slice(*possibilities[0]))
	try:
		for p in possibilities[1:]:
			retval.append(get_slice_trips(get_slice(*p)))
	except IndexError:
		pass
	return retval

def get_slice_trips(tslice):
	return tslice['response']['trips']['tripOption']

def get_slice(origin, dest, date):
	params = {
		"key": apikey
	}
	query = json.loads(basequery)
	query['request']['slice'][0]['origin'] = origin
	query['request']['slice'][0]['destination'] = dest
	query['request']['slice'][0]['date'] = date
	r = requests.post(
		baseurl,
		params = params,
		data = json.dumps(query),
		headers = headers
	)
	return json.loads(r.text)

if __name__ == '__main__':
	print get_routes('LAX,SFO', 'NRT,HKG', '2015-12-25,2015-12-26')
