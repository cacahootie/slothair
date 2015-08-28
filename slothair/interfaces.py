
import os.path
import json

import requests

baseurl = "https://www.googleapis.com/qpxExpress/v1/trips/search"
headers = {'content-type': 'application/json'}

basedir = os.path.dirname(os.path.abspath(__file__))
keypath = os.path.join(basedir,'apikey')
apikey = open(keypath).read()
basequery = open(os.path.join(basedir,'templates','search_request.json')).read()

def get_qpx(origin, dest, date):
	params = {
		"key": apikey
	}
	query = json.loads(basequery)
	print query
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
	print get_qpx('LAX', 'NRT', '2015-12-25')
