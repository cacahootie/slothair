var map,
    display_layer,
    source_layer;

function draw_map (d) {
	
}

var attrtext = '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors | <a href="http://openflights.org">OpenFlights</a>'

var BaseView = Backbone.View.extend({
    initialize: function(){
        this.render();
    },
    data: null,
    render: function () {
        if (this.data) {
            try {
                this.$el.html(Mustache.to_html(this.template,this.data.toJSON()));
            } catch (e) {
                this.$el.html(Mustache.to_html(this.template,this.data));
            }
        }
        else this.$el.html(this.template);
        return this;
    }
});


var AppView = BaseView.extend({
    el: '#container',
    template: $("#layout").html(),
    initialize: function() {
    	BaseView.prototype.initialize.call(this);
        this.header = new HeaderView();
        this.mapviewview = new MapviewView();
        this.mapview = new MapView();
        this.resultsview = new ResultsView();
        return this;
    }
});


var HeaderView = BaseView.extend({
    template: $("#header_templ").html()
});


var MainView = BaseView.extend({
    el: '#main'
});


var MapState = Backbone.Model.extend({
    defaults: {
        mapCenter: [33, -112],
        mapZoom: 4
    }
});


var MapviewView = MainView.extend({
	template: $("#mapview_templ").html(),
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
    initialize: function () {
        BaseView.prototype.initialize.call(this);
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
    select_route: function(d) {
        var self = this;
        d3.json('/airport/'+d, function got_airport (d) {
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

            var detail = d.name + '<br />' + d.iata_faa_id;
            d3.select('#info').html("From " + detail);

            d3.json('/routes/' + d.iata_faa_id, function (d) {
                self.load_layer(d);
            });
        })
    },
    load_layer: function(d) {
        results.data = d
        var map = this.map;
    	var display_layer = this.display_layer;
    	try {
            map.removeLayer(display_layer);
        } catch (e) {  }
		display_layer = L.layerGroup();

		var center = map.getCenter().lng;

		if (center < 0) {
			this.lng_offset = center + 180;
		} else {
			this.lng_offset = 180 - center;
		}

		d['results'].forEach(function(dd) {
			var detail = dd.name + '<br />' + dd.iata_faa_id;
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


var ResultsView = BaseView.extend({
	el: '#results',
    template: $("#results_templ").html(),
    load_results: function(d, whichend) {
        var result_div = d3.select('#result_container');
        result_div.html('');
        d3.select("#results_title").text('Non Stop ' + whichend);
        
        d['results'].forEach(function(dd) {
            var detail = dd.name + '<br />' + dd.iata_faa_id;
            detail = '<a href="#routes/' + dd.iata_faa_id + '">' + detail + '</a>'
            result_div.append('div')
                .html(detail)
                .classed('result',true)
        })
    },
});


var AppRouter = Backbone.Router.extend({
    routes: {
        "":"home",
        "home":"home",
        "routes/:source":"rts",
    },
    loadView: function(view,params,coll) {
        $('#main').empty()
        this.view = new view(params);
    },
    hashChange : function(evt) {
        if(this.cancelNavigate) { // cancel out if just reverting the URL
            evt.stopImmediatePropagation();
            this.cancelNavigate = false;
            return;
        }
        if(this.view && this.view.dirty) {
            var dialog = confirm("You have unsaved changes. To stay on the page, press cancel. To discard changes and leave the page, press OK");
            if(dialog == true)
                return;
            else {
                evt.stopImmediatePropagation();
                this.cancelNavigate = true;
                window.location.href = evt.originalEvent.oldURL;
            }
        }
    },
    home: function () {
        var self = this;
        d3.json('/sources', function(d) {
            self.view.mapview.load_layer(d);
            self.view.resultsview.load_results(d, 'Origins');
        });
    },
    rts: function (source) {
        var self = this;
        d3.json('/routes/' + source, function(d) {
            self.view.mapview.select_route(source);
            self.view.resultsview.load_results(d, 'Destinations');
        });
    }
});


var base = new AppView();
var router = new AppRouter();
router.view = base;
$(window).on("hashchange", router.hashChange);
Backbone.history.start();
