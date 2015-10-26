var OriginResultsView = BaseView.extend({
    el:'#main',
    template: $("#search_results_templ"),
    initialize: function (querystring) {
        BaseView.prototype.initialize.call(this);
        var self = this;
        d3.text('/search/origin/?' + querystring, function (e,d) {
            $(self.el).append(d);
        })
    }
});

var OriginSearchView = BaseView.extend({
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
                international: {
                    type: "boolean"
                },
                departure: {
                    type: "string",
                    format: "date"
                },
                return_: {
                    type: "string",
                    label:"return date",
                    format: "date",
                    optional: true
                },
                booking_class: {
                    type: "string",
                    enum: ["COACH","PREMIUM_COACH","BUSINESS","FIRST"]
                },
                numresults: {
                    type: "string",
                    format: "number",
                    default: 50
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
            var query = editor.getValue();
            if (query.result_format == 'html') {
                window.location.href = "#origin_results?" + $.param(query);
            } else {
                window.location.href = "/search/origin/?" + $.param(query);
            }
        });
    }
});