
def duration(result):
	duration = 0
	for slc in result['slice']:
		duration += int(slc['duration'])
	return duration

sorters = {
	'price': lambda x: float(x['saleTotal'].replace('USD','')),
	'duration':duration
}