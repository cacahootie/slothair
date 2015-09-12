from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField, SelectField

class FlightSearchForm(Form):
	origin = StringField('From')
	dest = StringField('To')
	date = StringField('Travel Date')
	numresults = IntegerField('Number of Results', default = 10)
	sortby = SelectField('Sort By', choices = [
		('price', 'Price'),
		('duration', 'Duration'),
	])
