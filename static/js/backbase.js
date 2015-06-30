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


var HeaderView = BaseView.extend({
    template: $("#header_templ").html()
});


var MainView = BaseView.extend({
    el: '#main'
});