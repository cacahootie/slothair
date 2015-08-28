from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField

class FlightSearchForm(Form):
	origin = StringField('From')
	dest = StringField('To')
	date = StringField('Travel Date')
	numresults = IntegerField('Number of Results')