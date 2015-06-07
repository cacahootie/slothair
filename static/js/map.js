$(window).load(function () {
	// create a map in the "map" div, set the view to a given place and zoom
	var map = L.map('map').setView([30, -110], 6);

	// add an OpenStreetMap tile layer
	L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
	    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
	}).addTo(map);

	d3.json('/sources', function(d) {
		d['sources'].forEach(function(dd) {
			console.log(dd);
			L.marker([dd['lat'],dd['lng']])
				.bindPopup(dd)
				.addTo(map);
		})
	})
})