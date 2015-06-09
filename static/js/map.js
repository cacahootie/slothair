var map,
    display_layer,
    source_layer;

function draw_map (d) {
	if (display_layer) map.removeLayer(display_layer);

	display_layer = L.layerGroup();
	var result_div = d3.select('#result_inner');
	result_div.html('')

	d['results'].forEach(function(dd) {
		result_div.append('div')
			.html(dd.name + '<br />' + dd.city + '<br />' + dd.iata_faa_id)
			.classed('result',true)

		L.marker([dd.lat,dd.lng])
			.bindPopup(dd.iata_faa_id)
			.on('mouseover', function show_tooltip () { this.openPopup(); })
			.on('mouseout', function hide_tooltip () { this.closePopup(); })
			.on('click', function map_click () {
				try { map.removeLayer(source_layer); } catch (e) {}

				source_layer = L.layerGroup();
				
				var circle = L.circleMarker([dd.lat, dd.lng], {
					color: 'red',
					radius: 20,
					weight: 10,
					fillColor: 'green',
					fillOpacity: 0.5
				}).addTo(source_layer)

				source_layer.addTo(map);

				d3.select('#info').html(
					"Non Stop from <br />" + dd.name + '<br />' + dd.city
					+ '<br />' + dd.country
				);

				d3.json('/routes/' + dd.iata_faa_id, draw_map);
			})
			.addTo(display_layer);
	})

	display_layer.addTo(map);
}

$(window).load(function () {
	map = L.map('map').setView([30, -110], 6);
	L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
	    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
	}).addTo(map);
	d3.json('/sources', draw_map);
})