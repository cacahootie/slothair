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