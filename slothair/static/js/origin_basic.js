var OriginSearchView = BaseView.extend({
    el:'#main',
    template: $("#search_results_templ"),
    initialize: function (querystring) {
        BaseView.prototype.initialize.call(this);
        var self = this;
        d3.text('/search/results/?' + querystring, function (e,d) {
            $(self.el).append(d);
        })
    }
});
