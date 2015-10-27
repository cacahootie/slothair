var attrtext = '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors | <a href="http://openflights.org">OpenFlights</a>';

var AppView = BaseView.extend({
    el: '#container',
    template: $("#layout").html(),
    initialize: function() {
    	BaseView.prototype.initialize.call(this);
        this.header = new HeaderView();
    }
});

var AppRouter = Backbone.Router.extend({
    routes: {
        "":"origins",
        "routes/:origin":"rts",
        "basic_search":"basic_search",
        "basic_results?*querystring":"basic_results",
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
        this.loadView(MapResultsView,{
            url:'/origins/',
            label: 'Origins'
        })
    },
    rts: function (origin) {
        this.loadView(MapResultsView,{
            url:'/routes/' + origin,
            label: 'Destinations',
            origin: origin
        })
    },
    basic_search: function () {
        this.loadView(SearchView,{});
    },
    basic_results: function (querystring) {
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