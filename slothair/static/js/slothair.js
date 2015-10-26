var attrtext = '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors | <a href="http://openflights.org">OpenFlights</a>';

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

var AppRouter = Backbone.Router.extend({
    routes: {
        "":"origins",
        "routes/:source":"rts",
        "search":"search",
        "results?*querystring":"results",
        "origin_search":"origin_search",
        "origin_results?*querystring":"origin_results"
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
    origins: function () {
        var self = this;
        d3.json('/sources', function(d) {
            self.view.mapview.load_layer(d);
            self.view.resultsview.load_results(d, 'Origins');
        });
    },
    rts: function (source) {
        var self = this;
        d3.json('/routes/' + source, function(d) {
            self.view.mapview.select_route(d, source);
            self.view.resultsview.load_results(d, 'Destinations');
        });
    },
    search: function () {
        this.loadView(SearchView,{});
    },
    results: function (querystring) {
        this.loadView(AirfareResultsView,querystring);
    },
    origin_search: function () {
        this.loadView(OriginSearchView,{});
    },
    origin_results: function (querystring) {
        this.loadView(OriginResultsView,querystring);
    }
});

var base = new AppView();
var router = new AppRouter();
router.view = base;
$(window).on("hashchange", router.hashChange);
Backbone.history.start();