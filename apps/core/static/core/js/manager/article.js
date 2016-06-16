/**
 * Created by maxbook on 02/06/16.
 */

/****************   ARTICLE   ******************/

var Article = function (id, element) {
    this.element = element;
    this.id = id;

    this.isLike = function () {
        console.log(this.element.parent().children().last().attr('class').indexOf('favorite-active'));
        return !(this.element.parent().children().last().attr('class').indexOf('favorite-active') >= 0);
    };

    this.setLike = function (active, inactive) {
        console.log(this.isLike());
        var counter = this.element.parent().children('.counter');
        console.log(counter);
        query_action(this.id, this.isLike(), urls.like_manager);
        design(selector.like_icon, this.isLike(), counter, active, inactive);
    };

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

    this.isSearch = function () {
        return query(urls.search_manager, mode.read);
    };

    this.setSearch = function () {
        Article.query(urls.like_manager, mode.write);
    };

    this.setView = function () {
        query_action(this.id, true, urls.read_manager);
    };

    this.nextStepFeedback = function () {
        this.element.parent().hide();
        this.element.parent().parent().find('.step2').show();
    };

    this.backStepFeedback = function () {
        this.element.parent().hide();
        this.element.parent().parent().find('.step1').show();
    };

    this.giveNewFeedback = function () {
        this.element.parent().hide();
        this.element.parent().parent().find('.step1').show();
    };

    this.changeMarkFeedback = function () {
        var state = this.element.attr('class');
        var element = this.element;

        console.log(state);
        element.parent().find('.material-icons.selected').removeClass('selected').removeAttr('style');
        element.addClass('selected').attr('style', 'color: ' + window.Manager.getColorKB() + ' !important');
        // if (!state.hasClass('selected')) {
        //     state.removeClass('selected');
        // }

        // if (!state.indexOf('selected') >= 0) {
        //     element.parent().find('.mark').each(function () {
        //         if ($(this).attr('class').indexOf('selected') >= 0)
        //             $(this).attr('class', element.attr('class'));
        //     });
        //     element.attr('class', element.attr('class') + ' selected');
        // }
    };

    this.sendFeedback = function () {
        var feedback_choice = this.element.parent().parent().find('.selected').attr('id');
        var feedback_text = this.element.parent().find('#explainus').val();

        this.element.parent().hide();
        this.element.parent().parent().find('.step3').show();

        $.get(urls.send_feedback, {'id': this.id, 'feedback_choice': feedback_choice, 'feedback_text': feedback_text},
            function (data) {
            });
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
        var articleHTML = article(data['id'], data['title'], data['author'], data['desc'], data['ok'],
            data['pub_date'], data['tags'], data['read'], null, data['file_option']);
        var statsHTML = stats(data['id'], data['views'], data['useful'], data['loved'], data['bigup'],
            data['favorites']);

        // RENDER PDF or HTML
        $(selector.body_selector).empty().append(articleHTML);

        if (data['file_option'] == 'ok') {
            var url = data['file_url'];
            renderPDFfromUrl(url);
        }

        // APPEND HTML STAT
        $(selector.stats_selector).empty().append(statsHTML);

        // RENDER HTML or PDF
        if (data['attachements'] != '') {
            $('#attachments-menu-lower-right').webuiPopover({content: data['attachements'], placement: 'bottom-right'});
            $('.nb_attachments').append(data['nb_attachment']).show();
        } else {
            $('.nb_attachments').hide();
        }
        initColors(window.Manager.getPrimaryColor(), window.Manager.getSecondaryColor(), window.Manager.getImgUrl());
        render_article();
        resize_iframe();

    }; // OK


    var query = function (id) {
        $.get(urls.get_article,
            {'id': id},
            function (data) {
                results(data);
                var article = $('.content-article');

                article.readingTime({
                    readingTimeTarget: article.parent().find('.eta'),
                    wordCountTarget: article.parent().find('.word-count'),
                    wordsPerMinute: 275,
                    round: true,
                    lang: 'en'
                });

                var txt = article.parent().find('.eta').text();
                article.parent().find('.eta').empty().append(txt + ' read');
            }
        );
    };

    var design = function (element, state, object, active, inactive) {
        switch (element) {
            case selector.like_icon:
                if (state) {
                    object.attr('class', active || attrclass.liked);
                    object.text(parseInt(object.text()) + 1);
                }
                else {
                    object.attr('class', inactive || attrclass.unliked);
                    object.text(parseInt(object.text()) - 1);
                }
                break;
            case selector.read_icon:
                if (state)
                    object.css(active || style.read);
                else object.css(inactive || style.unread);
                break;
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

    var article = function (key, title, author, content, verified_article, date_publish, tags, read_article, attachments
        , file_option) {
        var color_read = (read_article == 'ok' ? 'color_bigup' : 'color_base');
        var readed = (read_article == 'ok' ? 'readed' : 'unreaded');
        var content_final = (file_option == 'ko' ? content : '<div id="svg-rendering"></div>');
        var ext_svg = (file_option == 'ko' ? '' : '-svg');

        return '<div class="article shadow_material">' +
            // '<div class="secondHeader">' +
            // '<span class="tags-section txt">' + tags + '</span>' +
            // '</div>' +
            '<header class="header-article">' +
            '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>' +
            '<span class="schedule-txt txt">' + date_publish + '</span>' +
            '<p><small><span class="eta"></span></small></p>' +
            '<span class="key" id="' + key + '" hidden="hidden">' + key + '</span>' +
            '<a class="article-title">' + title +
            '<i class="material-icons done_all_read ' + color_read + '">done_all</i></a>' +
            '</header>' +
            '<div class="content-article' + ext_svg + '">' + content_final + '</div>' +
            '<aside class="glossary-article">' + '</aside>' +
            '</div>';
    };

    var stats = function (key, view_counter, useful_counter, favorite_counter, bigup_article, favorites, attachments) {
        var active_bigup = (bigup_article == 'ok' ? 'bigup-active' : '');
        var active_favorite = (favorites == 'ok' ? 'favorite-active' : '');

        return '<div class="">' +
            '<span class="key" id="' + key + '" hidden="hidden">' + key + '</span>' +

            '<div class="stat-container like-button">' +
            '<i class="center-icon color_base_favorite favorite material-icons md-24 width24">favorite</i>' +
            '<span class="counter counter-like ' + active_favorite + '">' + favorite_counter + '</span>' +
            '</div>' +

            '<div class="stat-container bigup-button">' +
            '<i class="center-icon color_bigup useful material-icons md-24 width24">thumb_up</i>' +
            '<span class="counter counter-bigup ' + active_bigup + '">' + useful_counter + '</span>' +
            '</div>' +

            '<div class="stat-container view-button">' +
            '<i class="center-icon material-icons remove_red_eye color_base md-24 width24">remove_red_eye</i>' +
            '<span class="counter counter-view">' + view_counter + '</span>' +
            '</div>' +

            '<div class="stat-container attached-button">' +
            '<button id="attachments-menu-lower-right"' +
            ' class="mdl-button mdl-js-button mdl-button--icon" style="color: #C2C2CA;">' +
            '<i class="center-icon-attach attachment-button material-icons color_base md-24">attach_file</i>' +
            '</button>' +
            '<span class="nb_attachments"></span>' +
            '</div>' +

            '</div>';
    };

    var mode = {
        'read': 'r',
        'write': 'w'
    };

    var selector = {
        'body_selector': '.modal-body-article',
        'stats_selector': '.modal-stats-article',
        'comment_selector': '.modal-comments-article',
        'attachment_selector': '.modal-attachments-article',
        'like_selector': '.like-button',
        'like_icon': '.favorite',
        'read_selector': '.read-button',
        'bigup_selector': '.bigup-button',
        'bigup_icon': '.useful'
    };

    var attrclass = {
        'base': {},
        'liked': 'counter counter-like favorite-active',
        'unliked': 'counter counter-like',
        'unbigup': 'counter counter-bigup',
        'bigup': 'counter counter-bigup bigup-active'
    };

    var style = {
        'read': {},
        'unread': {}
    };

    var urls = {
        'like_manager': LIKE_MANAGER,
        'read_manager': READ_MANAGER,
        'bigup_manager': BIGUP_MANAGER,
        'search_manager': SEARCH_MANAGER,
        'get_article': GET_ARTICLE,
        'send_feedback': SEND_FEEDBACK
    };
};
