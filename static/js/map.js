var map,
    display_layer,
    source_layer,
    lng_offset = 50;

function draw_map (d) {
	if (display_layer) map.removeLayer(display_layer);
	display_layer = L.layerGroup();

	var result_div = d3.select('#result_container')
	result_div.html('')

	d['results'].forEach(function(dd) {
		var detail = dd.name + '<br />' + dd.iata_faa_id;
		result_div.append('div')
			.html(detail)
			.classed('result',true)

		var lng = dd.lng;
		if (lng > lng_offset) {
			lng = lng - 360;
		}

		L.circleMarker([dd.lat, lng], {
			color: 'red',
			fillColor: 'blue',
			radius: 10,
			weight: 5,
			fillOpacity: 0.5
		})
			.bindPopup(detail, {offset: L.point(0,-10)})
			.on('mouseover', function show_tooltip () { this.openPopup(); })
			.on('mouseout', function hide_tooltip () { this.closePopup(); })
			.on('click', function map_click () {
				try { map.removeLayer(source_layer); } catch (e) {}

				source_layer = L.layerGroup();

				var lng = dd.lng;
				if (lng > lng_offset) {
					lng = lng - 360;
				}
				
				var circle = L.circleMarker([dd.lat, lng], {
					color: 'red',
					radius: 14,
					weight: 10,
					fillColor: 'green',
					fillOpacity: 0.5
				}).addTo(source_layer)

				source_layer.addTo(map);

				d3.select('#info').html("From " + detail);

				d3.json('/routes/' + dd.iata_faa_id, draw_map);
			})
			.addTo(display_layer);
	})

	display_layer.addTo(map);
}

var attrtext = '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors | <a href="http://openflights.org">OpenFlights</a>'

$(window).load(function () {
	map = L.map('map').setView([30, -110], 6);
	L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
	    attribution: attrtext
	}).addTo(map);
	d3.json('/sources', draw_map);
})