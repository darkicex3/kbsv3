/**
 * Created by maxbook on 02/06/16.
 */

/****************   DAILY RECAP   ******************/

var DailyRecap = function (id, element) {

    this.element = element;
    this.id = id;

    this.isBigup = function () {
        return !(this.element.parent().children().last().attr('class').indexOf('bigup-active') >= 0);
    };

    this.setBigup = function (active, inactive) {
        console.log(this.isBigup());
        var counter = this.element.parent().children('.counter');
        console.log(counter);
        query_action(this.id, this.isBigup(), urls.bigup_manager);
        design(selector.bigup_icon, this.isBigup(), counter, active, inactive)
    };

    this.isRead = function () {
        return query(urls.read_manager, mode.read);
    };

    this.setRead = function (active, inactive) {
        query(urls.like_manager, mode.write);
        design(this.read_selector, this.isRead(), active, inactive);
    };

    this.setView = function () {
        query_action(this.id, true, urls.read_manager);
    };

    var query_action = function (id, bool, url) {
        $.get(url,
            {'id': id, 'action': bool},
            function (data) {

            }
        );
    };
    this.show = function () {
        query(this.id);
    }; // OK

    var results = function (data, display) {
        var result = '';

        // GET HTML
        var articleHTML = daily_recap(data['id'], data['title'], data['author'], data['desc'], data['ok'],
            data['pub_date'], data['tags'], data['read'], data['attachements'], data['file_option']);
        var statsHTML = daily_recap_stats(data['id'], data['views'], data['useful'], data['loved'], data['bigup'],
            data['favorites']);

        // RENDER PDF or HTML
        $(selector.body_selector).empty().append(articleHTML);

        // APPEND HTML STAT
        $(selector.stats_selector).empty().append(statsHTML);

        // RENDER HTML or PDF
        render_article();
        resize_iframe();
        initColors(window.Manager.getColorKB());

    }; // OK


    var query = function (id) {
        $.get(urls.show_daily_recap,
            {'id': id},
            function (data) {
                results(data);
                var dailyrecap = $('.content-daily-recap');

                dailyrecap.readingTime({
                    readingTimeTarget: dailyrecap.parent().find('.eta'),
                    wordCountTarget: dailyrecap.parent().find('.word-count'),
                    wordsPerMinute: 275,
                    round: true,
                    lang: 'en'
                });

                var txt = dailyrecap.parent().find('.eta').text();
                dailyrecap.parent().find('.eta').empty().append(txt + ' read');
            }
        );
    };

    var design = function (element, state, object, active, inactive) {
        switch (element) {
            case selector.bigup_icon:
                if (state) {
                    object.attr('class', active || attrclass.bigup);
                    object.text(parseInt(object.text()) + 1);
                }
                else {
                    object.attr('class', inactive || attrclass.unbigup);
                    object.text(parseInt(object.text()) - 1);
                }
                break;
            default:
                break;
        }
    };

    var daily_recap = function (key, title, author, content, verified_article, date_publish, tags, read_article, attachments) {
        var color_read = (read_article == 'ok' ? 'color_bigup' : 'color_base');
        var readed = (read_article == 'ok' ? 'readed' : 'unreaded');

        return '<div class="article shadow_material">' +
            '<div class="second-header-daily-recap">' +
            '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>' +
            '<span class="key" id="' + key + '" hidden="hidden">' + key + '</span>' +
            '<a class="title-daily-recap">' + title + '<i class="done_all_read material-icons color_base">done_all</i></a>' +
            '<span class="schedule-txt-dialy-recap txt">' + date_publish + '</span>' +
            '</div>' +
            '<div class="content-daily-recap content-article">' + content + '</div>' +
            '</div>';
    };

    var daily_recap_stats = function (key, view_counter, useful_counter, favorite_counter, bigup_article, favorites) {
        var active_bigup = (bigup_article == 'ok' ? 'bigup-active' : '');

        return '<div class="">' +
            '<span class="key" id="' + key + '" hidden="hidden">' + key + '</span>' +

            // '<div class="stat-container bigup-button">' +
            // '<i class="center-icon color_bigup useful material-icons md-24 width24">thumb_up</i>' +
            // '<span class="counter counter-bigup ' + active_bigup + '">' + useful_counter + '</span>' +
            // '</div>' +

            '<div class="stat-container view-button">' +
            '<i class="center-icon material-icons remove_red_eye color_base md-24 width24">remove_red_eye</i>' +
            '<span class="counter counter-view">' + view_counter + '</span>' +
            '</div>' +
            '</div>';
    };

    var mode = {
        'read': 'r',
        'write': 'w'
    };

    var selector = {
        'body_selector': '.modal-body-daily-recap',
        'stats_selector': '.modal-stats-daily-recap',
        'attachment_selector': '.modal-attachments-daily-recap',
        'bigup_selector': '.bigup-button',
        'bigup_icon': '.useful'
    };

    var attrclass = {
        'base': {},
        'unbigup': 'counter counter-bigup',
        'bigup': 'counter counter-bigup bigup-active'
    };

    var style = {
        'read': {},
        'unread': {}
    };

    var urls = {
        'read_manager': READ_MANAGER_DR,
        'bigup_manager': USEFUL_MANAGER_DR,
        'show_daily_recap': SHOW_DAILY_RECAP
    };
};
