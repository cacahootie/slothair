"""sort functions for qpxExpress"""

import dateutil.parser as dtparse

def isodate_time(value):
	return dtparse.parse(value).strftime('%H:%M')

def duration(value):
	hours = value // 60
	minutes = value - hours * 60
	return "%sh%sm" % (hours, minutes)
    