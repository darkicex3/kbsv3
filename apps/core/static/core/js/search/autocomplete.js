/**
 * Created by maxbook on 06/05/16.
 */
// In a perfect world, this would be its own library file that got included
// on the page and only the ``$(document).ready(...)`` below would be present.
// But this is an example.
$(document).ready(function () {

    var Autocomplete = function (options) {
        this.form_selector = options.form_selector;
        this.url = options.url || URL_AUTO_COMPLETE;
        this.delay = parseInt(options.delay || 300);
        this.minimum_length = parseInt(options.minimum_length || 1);
        this.form_elem = null;
        this.query_box = null;
    };

    Autocomplete.prototype.setup = function () {
        var self = this;

        this.form_elem = $(this.form_selector);
        this.query_box = this.form_elem.find('input[name=q]');
        // Watch the input box.
        this.query_box.on('keyup', function () {
            var query = self.query_box.val();

            if (query.length < self.minimum_length) {
                return false
            }

            self.fetch(query)
        });

        // On selecting a result, populate the search field.
        this.form_elem.on('click', '.ac-result', function (ev) {
            self.query_box.val($(this).text());
            $('.ac-results').remove();
            $('.cover').hide(100);
            return false
        })
    };

    Autocomplete.prototype.fetch = function (query) {
        var self = this;
        var tags = $('#search_categories').text();
        var sort = $('#search_sorting').text();

        if(tags.indexOf('#') != -1)
            tags = tags.slice(1);
        else
            tags = null;

        console.log(tags);

        window.Manager.getListArticle(tags, null, sort, null, true, query);
        // $.ajax({
        //     url: this.url
        //     , data: {
        //         'in': tags,
        //         'q': query,
        //         'by': sort
        //     }
        //     , success: function (data) {
        //         self.show_results(data);
        //         console.log(data);
        //     }
        // })
    };

    Autocomplete.prototype.show_results = function (data) {

        var results = data.results || [];

        if (results.length > 0) {
            
            console.log(results.length);
        }
        else {
            console.log('No results');
        }

    };


    window.autocomplete = new Autocomplete({
        form_selector: '.autocomplete-me'
    });
    window.autocomplete.setup();
});

function initColors(color) {
    $('#static-menu').attr('style','border-bottom:'+ color + ' 1px solid !important');
    $('.daily-recap-pubdate').attr('style','background-color:' + color + ' !important');
    $('.schedule-txt').attr('style','background-color:'+ color+ ' !important');
    $('.favorite').attr('style','color:'+ color+ '!important');
    $('.material-icons.selected').attr('style','color:'+ color+ ' !important');
    $('.nextq').attr('style','background:'+ color+ ' !important');
    $('.header_poll').attr('style','background:'+ color+ ' !important');
    $('.completed_survey').attr('style','color:'+ color+ ' !important');
    $('.color_favorites').attr('style','color:'+ color+ ' !important');
};