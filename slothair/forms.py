from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField, SelectField, \
	BooleanField

class FlightSearchForm(Form):
	origin = StringField('From')
	dest = StringField('To')
	date = StringField('Travel Date')
	refundable = BooleanField('Refundable')
	numresults = IntegerField('Number of Results', default = 10)
	sortby = SelectField('Sort By', choices = [
		('price', 'Price'),
		('duration', 'Duration'),
	])
	result_format = SelectField('Result Format', choices = [
		('html','HTML'),
		('json','JSON')
	])