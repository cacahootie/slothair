
import os.path
import json
from itertools import product
from operator import itemgetter
import datetime
from pprint import pprint

import requests
import dateutil.parser as dtparse
from flask import g
from requests_futures.sessions import FuturesSession

from sorters import sorters
from memoize import memoized
from slothair import models

session = FuturesSession()

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

def get_routes(origin, dest, departure, return_, numresults, refundable,
        booking_class):
    return get_multi(
        get_possibilities(
            origin,
            dest,
            departure,
            return_
        ),
        numresults,
        refundable,
        booking_class
    )

def get_origin_trips(origin, departure, return_, international, carrier):
    if international not in (None, False):
        dests = models.origin_routes_international(origin)['results']
    else:
        dests = models.origin_routes(origin)['results']
    return get_multi([
        (origin, dest, departure, return_)
        for dest in dests
    ], 50, False, "COACH", carrier)

def get_dates(dates):
    if dates is None:
        return []
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

def get_possibilities(origins, destinations, departure, return_):
    if return_ :
        return list(product(
            origins.split(','),
            destinations.split(','),
            get_dates(departure),
            get_dates(return_)
        ))
    return list(product(
            origins.split(','),
            destinations.split(','),
            get_dates(departure),
            [None]
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
                for leg in segment['leg']:
                    leg['aircraft_display'] = next(
                        x['name'] for x in data['aircraft'] 
                        if x['code'] == leg["aircraft"]
                    )
    return trips

def get_multi(possibilities, numresults, refundable, booking_class,
        carrier = None):
    try:
        futures = [
            get_slice(*p + (numresults, refundable, booking_class, carrier) )
            for p in possibilities
        ]
        trips, data = None, None
        for future in futures:
            subresult, p_data = get_slice_trips(
                future.result().json()
            )
            if subresult is None and p_data is None:
                continue
            if data is None:
                data = p_data
                trips = subresult
            else:
                update_data(data, p_data)
                trips += subresult
    except IndexError:
        pass
    return process_data(trips, data)

def get_slice_trips(tslice):
    try:
        return tslice['trips']['tripOption'], tslice['trips']['data']
    except KeyError:
        return None, None

def get_slice(origin, dest, departure, return_, numresults, refundable, 
        booking_class, carrier):
    params = {
        "key": apikey
    }
    query = json.loads(basequery)
    query['request']['slice'][0].update({
        'origin': origin,
        'destination': dest,
        'date': departure,
        'preferredCabin': booking_class if booking_class else "COACH",
        'permittedCarrier': [carrier]
    })
    if return_ is not None:
        query['request']['slice'].append({
            'origin': dest,
            'destination': origin,
            'date': return_,
            'preferredCabin': booking_class if booking_class else "COACH",
            'permittedCarrier': [carrier]
        })
    query['request']['solutions'] = numresults
    query['request']['refundable'] = refundable

    def bg_cb(sess, resp):
        # parse the json storing the result on the response object
        resp.data = json.loads(resp.text)
        if 'error' in resp.data:
            print resp.text
            raise ValueError

    return session.post(
        baseurl,
        params = params,
        data = json.dumps(query),
        headers = headers
    )

if __name__ == '__main__':
    print get_routes('LAX,SFO', 'NRT,HKG', '2015-12-25,2015-12-26', 10)
