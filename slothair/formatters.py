"""format tags for slothair"""

import dateutil.parser as dtparse

def isodate_time(value):
	return dtparse.parse(value).strftime('%a %x %H:%M')

def duration(value):
	hours = value // 60
	minutes = value - hours * 60
	return "%sh%sm" % (hours, minutes)
    
def currency_symbol(value):
	if value.startswith('USD'):
		return value.replace('USD','$',1)
