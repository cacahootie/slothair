var map;

function draw_map (d) {
	try {
		map.remove();
	} catch (e) {
		console.log('lol')
	}
	map = L.map('map').setView([30, -110], 6);

	L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
	    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
	}).addTo(map);

	d['results'].forEach(function(dd) {
		L.marker([dd['lat'],dd['lng']])
			.on('click', function map_click () {
				d3.select('#info_window').text(dd.name);
				d3.json('/routes/' + dd.iata_faa_id, draw_map);
			})
			.addTo(map);
	})
}

$(window).load(function () {
	d3.json('/sources', draw_map);
})