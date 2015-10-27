
var MapState = Backbone.Model.extend({
    defaults: {
        mapCenter: [33, -112],
        mapZoom: 4
    }
});


var MapviewView = MainView.extend({
	template: $("#mapview_templ").html(),
});


var MapResultsView = BaseView.extend({
    el: '#main',
    template: $("#mapview_templ").html(),
    initialize: function (params) {
        BaseView.prototype.initialize.call(this)
        var results_url = params.url,
            results_label = params.label,
            origin = params.origin
        var self = this
        d3.json(results_url, function(d) {
            self.mapview = new MapView(d)
            if (origin) {
                self.mapview.select_route(d, origin)
            }
            self.resultsview = new ResultsView(d, results_label)
        })
    }
});

var MapState = new MapState();
var MapView = BaseView.extend({
    el: '#map',
    map: null,
    settings: {},
    set_state: function (e) {
        MapState.set('mapCenter', this.map.getCenter());
        MapState.set('mapZoom', this.map.getZoom());
    },
    initialize: function (route_layer) {
        BaseView.prototype.initialize.call(this)
        this.load_layer(route_layer)
    },
    render: function(){
        var mapCenter = MapState.get('mapCenter');
        var mapZoom = MapState.get('mapZoom');
        this.map = L.map(
            'map', this.settings
        ).setView(mapCenter, mapZoom);
        
        underlay = L.tileLayer(
            'https://otile1-s.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.png'
        ).addTo(this.map);
        
        var self = this;
        this.map.on('dragend', function (e) {
            self.set_state(e);
        });
        return this;
    },
    display_layer: false,
    source_layer: false,
    select_route: function(routes, source) {
        var self = this;
        d3.json('/airport/'+source, function got_airport (d) {
            if(self.source_layer) { self.map.removeLayer(self.source_layer); }
            self.source_layer = L.layerGroup();

            var lng = d.lng;
            if (lng > self.lng_offset) {
                lng = lng - 360;
            }

            self.map.setView([d.lat,lng])
            var circle = L.circleMarker([d.lat, lng], {
                color: 'red',
                radius: 14,
                weight: 10,
                fillColor: 'green',
                fillOpacity: 0.5
            }).addTo(self.source_layer)

            self.source_layer.addTo(self.map);

            var detail = d.name + '<br />(' + d.iata_faa_id + ')';
            d3.select('#info').html(detail);

            self.load_layer(routes, d.lat);
        })
    },
    load_layer: function(d, center) {
        results.data = d
        var map = this.map;
    	var display_layer = this.display_layer;
    	try {
            map.removeLayer(display_layer);
        } catch (e) {  }
		display_layer = L.layerGroup();

		if (!center) center = map.getCenter().lng;

		if (center < 0) {
			this.lng_offset = center + 180;
		} else {
			this.lng_offset = 180 - center;
		}

		d['results'].forEach(function(dd) {
			var detail = dd.name + '<br />(' + dd.iata_faa_id + ')';
            detail = '<a href="#routes/' + dd.iata_faa_id + '">' + detail + '</a>'
			
			var lng = dd.lng;
			if (lng > this.lng_offset) {
				lng = lng - 360;
			}

			var mk = L.circleMarker([dd.lat, lng], {
				color: 'red',
				fillColor: 'blue',
				radius: 10,
				weight: 5,
				fillOpacity: 0.5
			}).addTo(display_layer);
			
            var self = this;
            mk.bindPopup(detail, {offset: L.point(0,-10)})
				.on('mouseover', function show_tooltip () { this.openPopup(); })
				.on('mouseout', function hide_tooltip () { this.closePopup(); })
				.on('click', function map_click () {
					router.navigate('routes/' + dd.iata_faa_id, true)
				})
		})

		display_layer.addTo(map);
        this.display_layer = display_layer;
    }
});
