var AirfareResultsView = BaseView.extend({
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

var SearchView = BaseView.extend({
    el:'#main',
    template: $("#search_form").html(),
    initialize: function () {
        BaseView.prototype.initialize.call(this);
        var editor = new JSONEditor(document.getElementById('editor_holder'),{
            ajax: true,
            theme: "bootstrap3",
            disable_properties: true,
            disable_edit_json: true,
            disable_collapse: true,
            schema: {
              type: "object",
              title: "Airfare Search",
              properties: {
                origin: {
                    "$ref": "/forms/sourcelist"
                },
                destination: {
                    "$ref": "/forms/sourcelist"
                },
                departure: {
                    type: "string",
                    format: "date"
                },
                numresults: {
                    type: "string",
                    format: "number",
                    default: 10
                },
                refundable: {
                    type: "boolean"
                },
                sortby: {
                    type: "string",
                    enum: ["price", "duration"]
                },
                result_format: {
                    type: "string",
                    enum: ["html","json"]
                }
              }
            }
          });
      
        document.getElementById('submit').addEventListener('click',function() {
            window.location.href = "#results?" + $.param(editor.getValue());
        });
    }
});
