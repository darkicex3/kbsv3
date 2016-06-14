/**
 * Created by maxbook on 19/05/16.
 */

/****************      ARTICLE MANAGER    ******************/

var ArticleManager = function (options) {
    var results_selector = '.main-content';
    var results_daily_selector = '.daily-recap-module .content-module';
    var results_tags_selector = '.most-popular-tags-module .content-module';
    var results_poll_selector = '.survey-module .content-module';
    var link_article_selector = '.link-title-article';
    var daily_recap_selector = '.daily-recap-title';
    var daily_recap_feed_selector = '.main-content-daily-recap';
    var poll_selector = '.link-poll';
    var attachment_selector = '';
    var result = 0;
    var progress = 0;
    var current_score_survey = 0;
    var current_article = null;
    var current_daily_recap = null;
    var current_poll = null;
    this.current_id = null;
    this.display = 'list';
    this.counter = 20;
    this.category = 'Home';
    this.autoquery = null;
    this.autocomplete = false;
    this.sorting = 'publish_date';
    var colorKB = '';

    this.setColorKB = function (color) {
        colorKB = color;
    };

    this.getColorKB = function () {
        return colorKB;
    };
    
    this.getListArticle = function (category, tags, sorting, counter, autocomplete, autoquery) {
        query(category || this.category, tags, counter || this.counter, sorting || this.sorting,
            autocomplete || this.autocomplete, autoquery || this.autoquery);
    };

    this.getSearchSuggestions = function () {

    };

    this.getPopularTags = function () {
        var html = '';
        $.get(urls.get_popular_tags, {}, function (data) {
            for (var key in data) if (data.hasOwnProperty(key)) {
                html += '<span class="bookmarkBadge"><a id="#' + data[key] + '" class="bookmarkLink" href="#">' + data[key] +
                    '</a></span>'
            }
            $(results_tags_selector).empty().append(html);
        });
    };

    this.getListDailyRecap = function (sorting, from_date, nb) {
        query_daily_recap(sorting || null, from_date || null, nb || 100);
    };

    this.getListPolls = function (sorting, id, nb) {
        query_polls(sorting || null, id || null, nb || 100);
    };

    this.initEvents = function () {
        window.body.on("click", link_article_selector, function () {
            article($(this))
        });

        window.body.on("click", daily_recap_selector, function () {
            daily_recap($(this))
        });

        window.body.on("click", poll_selector, function () {
            poll($(this))
        });

        for (var element in selector_action) if (selector_action.hasOwnProperty(element))
            window.body.on("click", selector_action[element], function () {
                console.log($(this));
                action($(this))
            });
    };

    var query_polls = function (sorting, id, nb) {
        $.ajax({
            url: urls.get_polls,
            beforeSend: function () {
                $(results_poll_selector).empty().append('<div class="loading mdl-spinner mdl-js-spinner is-active"></div>');
            },
            data: {
                'sorting': sorting,
                'id': id,
                'nb': nb
            },
            success: function (data) {
                results_polls(data);
                Pace.restart();
            },
            error: function () {
                $(results_poll_selector).empty().append('<i class="error_xhr material-icons">flash_off</i>');
            }
        });
    };

    var query_daily_recap = function (sorting, from_date, nb) {
        $.ajax({
            url: urls.get_list_daily_recap,
            beforeSend: function () {
                $(results_daily_selector).empty().append('<div class="loading mdl-spinner mdl-js-spinner is-active"></div>');
            },
            data: {
                'sorting': sorting,
                'from': from_date,
                'nb': nb
            },
            success: function (data) {
                results_daily_recap(data);
                Pace.restart();
            }
        });
    };

    var query = function (category, tags, sorting, counter, autocomplete, autoquery) {
        $.ajax({
            url: urls.get_list_articles,
            beforeSend: function () {
                $(results_selector).empty().append('<div class="loading mdl-spinner mdl-js-spinner is-active"></div>');
            },
            data: {
                'by': category,
                'counter': counter,
                'sorting': sorting,
                'autocomplete': autocomplete,
                'autoquery': autoquery
            },
            success: function (data) {
                results(data);
                Pace.restart();
            }
        });
    };

    var article = function (object) {
        var article = new Article(object.parent().parent().attr("id"), object.parent().parent());
        console.log(object.parent().attr("id"), object.parent());
        current_article = article;
        article.setView();
        article.show();
    };

    var daily_recap = function (object) {
        var daily_recap = new DailyRecap(object.parent().attr("id"), object);
        current_daily_recap = daily_recap;
        daily_recap.setView();
        daily_recap.show();
    };

    var poll = function (object) {
        var poll = new Poll(object.parent().attr("id"), object);
        result = 0;
        progress = 0;
        current_score_survey = 0;
        current_poll = poll;
        poll.show();
    };

    var restartPoll = function () {
        result = 0;
        progress = 0;
        $('.result-poll').remove();
        $('.restart-poll').remove();
        $('.show-results-poll').remove();
        $('.body-poll').children('#question1').show();
    };

    var showResultsPolls = function () {
        console.log('3efrih3bg');
        $('.restart-poll').remove();
        $('.show-results-poll').remove();
        $('.question-poll').show();

        $('.choice').each(function () {
            $(this).removeClass('choice').addClass('res');
        });
        $('.wc1').each(function () {
            $(this).css('background', '#000');
        });
    };

    var styleChoice = function (obj) {
        style_choice(obj);
    };

    var nextQuestion = function (object) {

        var next_question = parseInt(object.parent().parent().children('.body-poll').children('div:visible').attr('id').replace('question', '')) + 1;
        var question_number = object.parent().find('.nb_questions').attr('id');

        var active_right_choices = $('#question' + (next_question - 1)).fadeOut(0, function () {
            $('#question' + next_question).fadeIn(200);
        }).find('.choice.active-choice.wc0');

        var right_choice_number = parseInt(object.parent().find('.nb_choice_right').attr('id'));

        current_score_survey += active_right_choices.length;

        console.log('pollFinalResult: ', current_score_survey, right_choice_number);


        if (next_question - 1 == question_number) {
            $('#question' + next_question).hide();
            $('.nextq').hide();
            pollFinalResult(current_score_survey, right_choice_number);
        }
    };

    var pollFinalResult = function (active_right_choices, right_choice_number) {
        var mark = ( active_right_choices / right_choice_number ) * 20;

        if (mark == 20) {
            $('<div class="result-poll">Perfect</div>' +
                '<div class="restart-poll mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent res">Restart</div>' +
                '<div class="show-results-poll mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect res">Show Results</div>'
            ).insertBefore("#question1");
        } else {
            $('<div class="result-poll">' + mark + '/20</div>' +
                '<div class="restart-poll mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent res">Restart</div>' +
                '<div class="show-results-poll mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect res">Show Results</div>'
            ).insertBefore("#question1");
        }
    };


    // .children('.choice').each(function () {
    //     console.log($(this).attr('class'));
    // }));
    // var classNextQuestion = 'question' + (parseInt(object.parent().parent().attr('id').replace('question', '')) + 1);

    // $(object.parent().parent()).fadeOut(200, function () {
    //     var nextQuestion = $('#' + classNextQuestion);
    //     var choice_id = object.attr('id');
    //     var number_of_question = object.parent().parent().parent().parent().find('.nb_questions').attr('id');
    //     var progress_bar_speed = 100 / number_of_question;
    //     var progress_bar = $('.progress-bar-poll');
    //
    //     $.get(urls.wrong_or_right, {'choice_id': choice_id}, function (data) {
    //         var pts_per_question = 20;
    //         console.log(data['ok']);
    //         if (data['ok'] == 'ok') {
    //             result += pts_per_question;
    //         }
    //
    //         console.log(result);
    //
    //         if (typeof nextQuestion.attr('id') == 'undefined') {
    //             progress_bar.css('width', '100%');
    //             console.log(number_of_question, result, pts_per_question);
    //             var score = (result / (number_of_question * pts_per_question)) * 20;
    //
    //             if (score == 20) {
    //                 $('<div class="result-poll">Perfect</div>' +
    //                     '<div class="restart-poll mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent res">Restart</div>' +
    //                     '<div class="show-results-poll mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect res">Show Results</div>'
    //                 ).insertBefore("#question1");
    //             } else {
    //                 $('<div class="result-poll">' + parseInt(score) + '/20</div>' +
    //                     '<div class="restart-poll mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent res">Restart</div>' +
    //                     '<div class="show-results-poll mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect res">Show Results</div>'
    //                 ).insertBefore("#question1");
    //             }
    //         } else {
    //             progress += progress_bar_speed;
    //             progress_bar.css('width', progress + '%');
    //         }
    //     });
    //
    //     nextQuestion.show(100);
    // });

    var action = function (object) {
        if (current_article)
            current_article.element = object;
        else if (current_daily_recap)
            current_daily_recap.element = object;
        else if (current_poll)
            current_poll.element = object;

        if (typeof object.attr('id') == 'undefined')
            object.attr('id', " ");



        // SEARCH
        if (object.attr('id').indexOf('search') >= 0)
            window.Manager.getSearchSuggestions();

        // ACTION ARTICLE
        if (object.attr('class').indexOf('favorite') >= 0)
            current_article.setLike();
        else if (object.attr('class').indexOf('choice') >= 0)
            styleChoice(object);
        else if (object.attr('class').indexOf('nextq') >= 0)
            nextQuestion(object);
        else if (object.attr('class').indexOf('useful') >= 0)
            current_article.setBigup();

        // ARTICLES TEMPLATE FILTER
        else if (object.attr('id').indexOf('home') >= 0) {
            window.Manager.getListArticle();
            design_top_menu(object);
        }
        else if (object.attr('class').indexOf('color-explicit') >= 0) {
            console.log('gros seins');
            window.Manager.getListArticle('Essential');
            design_top_menu('.essentials-button');
        }
        else if (object.attr('id').indexOf('essentials') >= 0) {
            console.log('gros seins');
            window.Manager.getListArticle('Essential');
            design_top_menu(object);
        }
        else if (object.attr('id').indexOf('most_popular') >= 0) {
            window.Manager.getListArticle('Most Viewed');
            design_top_menu(object);
        }
        else if (object.attr('id').indexOf('new') >= 0) {
            window.Manager.getListArticle('Recent');
            design_top_menu(object);
        }

        //DAILY_RECAPS_TEMPLATES
        else if (object.attr('class').indexOf('more_daily_recap') >= 0) {
            window.Manager.getListDailyRecap('any_date');
            window.Manager.display = 'card';
        }
        else if (object.attr('id').indexOf('all_daily_recaps') >= 0) {
            window.Manager.getListDailyRecap('any_date');
            window.Manager.display = 'card';
            design_top_menu_daily_recaps(object);
        }
        else if (object.attr('id').indexOf('last_7_days') >= 0) {
            window.Manager.getListDailyRecap('past_7_days');
            window.Manager.display = 'card';
            design_top_menu_daily_recaps(object);
        }
        else if (object.attr('id').indexOf('today') >= 0) {
            window.Manager.getListDailyRecap('today');
            window.Manager.display = 'card';
            design_top_menu_daily_recaps(object);
        }
        else if (object.attr('id').indexOf('unread') >= 0) {
            window.Manager.getListDailyRecap('unread');
            window.Manager.display = 'card';
            design_top_menu_daily_recaps(object);
        }
        else if (object.attr('id').indexOf('read') >= 0) {
            window.Manager.getListDailyRecap('read');
            window.Manager.display = 'card';
            design_top_menu_daily_recaps(object);
        }
        else if (object.attr('id').indexOf('most_view') >= 0) {
            window.Manager.getListDailyRecap('most_view');
            window.Manager.display = 'card';
            design_top_menu_daily_recaps(object);
        }

        // FEEDBACK ARTICLE
        else if (object.attr('class').indexOf('button-next-step-feedback') >= 0)
            current_article.nextStepFeedback();
        else if (object.attr('class').indexOf('button-back-step-feedback') >= 0)
            current_article.backStepFeedback();
        else if (object.attr('class').indexOf('button-step3-step-feedback') >= 0)
            current_article.giveNewFeedback();
        else if (object.attr('class').indexOf('mark') >= 0)
            current_article.changeMarkFeedback();
        else if (object.attr('class').indexOf('submit-feedback') >= 0)
            current_article.sendFeedback();

        // POLLS FILTER
        else if (object.attr('class').indexOf('restart-poll') >= 0)
            restartPoll();
        else if (object.attr('class').indexOf('show-results-poll') >= 0)
            showResultsPolls();
        else if (object.attr('class').indexOf('any_date_p') >= 0)
            window.Manager.getListPolls('any_date');
        else if (object.attr('class').indexOf('past_7_days_p') >= 0)
            window.Manager.getListPolls('past_7_days');
        else if (object.attr('class').indexOf('this_month_p') >= 0)
            window.Manager.getListPolls('this_month');
        else if (object.attr('class').indexOf('this_year_p') >= 0)
            window.Manager.getListPolls('this_year');
        else if (object.attr('class').indexOf('today_p') >= 0)
            window.Manager.getListPolls('today');

        // DAILY RECAP FILTER
        else if (object.attr('class').indexOf('any_date') >= 0)
            window.Manager.getListDailyRecap('any_date');
        else if (object.attr('class').indexOf('past_7_days') >= 0)
            window.Manager.getListDailyRecap('past_7_days');
        else if (object.attr('class').indexOf('this_month') >= 0)
            window.Manager.getListDailyRecap('this_month');
        else if (object.attr('class').indexOf('this_year') >= 0)
            window.Manager.getListDailyRecap('this_year');
        else if (object.attr('class').indexOf('today') >= 0)
            window.Manager.getListDailyRecap('today');
    };

    var results = function (data, display) {
        var result = '';

        for (var key in data) if (data.hasOwnProperty(key))
            result += list(data[key]['id'], data[key]['title'], data[key]['desc'], data[key]['pub_date'],
                data[key]['loved'], data[key]['tags'], data[key]['favorites'], data[key]['read'],
                data[key]['useful'], data[key]['bigup'], data[key]['modified'], data[key]['views'],
                data[key]['url_option'], data[key]['url'], data[key]['attachments'], data[key]['newart'],
                data[key]['essential'], data[key]['nb_attachment']);


        $(results_selector).empty().append(result).parent().parent().parent().show();
        initColors(window.Manager.getColorKB());

        $('.att').click(function () {
            var e = $(this);
            $.get(GET_ATTACHMENTS, {'id': e.parent().parent().attr('id')}, function (data) {
                console.log(e);
                e.webuiPopover({
                    width: '300',
                    title: 'Attachments',
                    content: data['attachments'],
                    animation: 'pop',
                    closeable: 'true'
                }).webuiPopover('show');
            });
        });
    };

    var results_polls = function (data, display) {
        var result = '';
        for (var key in data) if (data.hasOwnProperty(key)) {
            var questions = data[key]['questions'];
            result += list_polls(key, data[key]['poll_title'], data[key]['nb_question'],
                data[key]['current_question']);
        }

        $(results_poll_selector).empty().append(result);
        initColors(window.Manager.getColorKB());
    };

    var results_daily_recap = function (data) {
        var result = '';

        for (var key in data) if (data.hasOwnProperty(key))
            if (window.Manager.display == 'card')
                result += list_daily_recap_card(data[key]['id'], data[key]['title'], data[key]['desc'], data[key]['pub_date'],
                    data[key]['loved'], data[key]['tags'], data[key]['favorites'], data[key]['read'],
                    data[key]['useful'], data[key]['bigup'], data[key]['modified'], data[key]['views'],
                    data[key]['url_option'], data[key]['url']);
            else
                result += list_daily_recap(data[key]['id'], data[key]['title'], data[key]['desc'], data[key]['pub_date'],
                    data[key]['loved'], data[key]['tags'], data[key]['favorites'], data[key]['read'],
                    data[key]['useful'], data[key]['bigup'], data[key]['modified'], data[key]['views'],
                    data[key]['url_option'], data[key]['url']);

        if (window.Manager.display == 'card')
            $(daily_recap_feed_selector).empty().append(result);
        else
            $(results_daily_selector).empty().append(result);
        initColors(window.Manager.getColorKB());
    };

    var list_polls = function (poll_id, poll_title, nb_questions, current_question) {
        return '<div class="mini-survey" id="' + poll_id + '">' +
            '<a data-toggle="modal" class="link-poll survey-title" href="#display-poll">' + poll_title + '</a>' +
            '<div class="nb_questions_completed '+(current_question == nb_questions ? 'completed_survey' : '')+'">'+current_question+'/'+nb_questions+'</div>' +
            '</div>';
    };

    var list_daily_recap = function (key, title, description, date_publish, favorite_counter, tags, favorites, read_article,
                                     useful_counter, bigup_article, last_update, view_counter, url_option, url) {

        return '<div class="mini-daily-recap" id="' + key + '">' +
            '<a class="daily-recap-title" data-toggle="modal" href="#display-daily-recap">' +
            title + '</a>' +
            '<div class="daily-recap-pubdate">' + date_publish + '</div>' +
            '</div>';
    };

    var list_daily_recap_card = function (key, title, description, date_publish, favorite_counter, tags, favorites, read_article,
                                          useful_counter, bigup_article, last_update, view_counter, url_option, url, newdaily) {

        return '<div class="card mini-daily-recap-card" id="' + key + '">' +
            '<div class="card-illustration"></div>' +
            '<div class="card-header padding">' + title + '</div>' +
            '<div class="card-stat">' +
            '<div class="like-wrapper stat-wrapper">' +
            '<i id="like-icon" class="color-base material-icons icon-mini-article">schedule</i>' +
            '<span id="like-counter" class="counter-wrapper">' + date_publish + '</span>' +
            '</div>' +
            '<div class="bigup-wrapper stat-wrapper">' +
            '<i id="bigup-icon" class="color-base material-icons icon-mini-article">thumb_up</i>' +
            '<span id="bigup-counter" class="counter-wrapper">' + useful_counter + '</span>' +
            '</div>' +
            '<div class="view-wrapper stat-wrapper">' +
            '<i id="view-icon" class="color-base material-icons icon-mini-article">visibility</i>' +
            '<span id="view-counter" class="counter-wrapper">' + view_counter + '</span>' +
            '</div>' +
            '</div>' +
            '<div class="card-action padding" style="display: none">ACTION</div>' +
            '<div class="card-status">' +
            (newdaily ? '<i class="color-new material-icons">fiber_new</i>' : '') +
            '</div>' +
            '</div>';
    };

    var list = function (key, title, description, date_publish, favorite_counter, tags, favorites, read_article,
                         useful_counter, bigup_article, last_update, view_counter, url_option, url, att, newart,
                         essential, nb_attachment) {
        // var attr_new = (newart == 'new' ? '<span class="id-article" style="">New</span><span class="id-article-ess" style="">Essential</span></td>' : '');
        // var attr_att = (att != '' ? ' attr_att' : '');
        //
        var href = (url_option == 'ok' ? url : '#display-article');
        var redirect = (url_option == 'ok' ? '_blank' : '');
        var classattr = (url_option == 'ok' ? 'link-title-article-url' : 'link-title-article');
        var liked_attr = (favorites == 'ok' ? 'color_favorites' : '');

        if (nb_attachment > 0) {

        }
        return '<div class="card mini-article" id="' + key + '">' +
            '<div class="card-illustration"></div>' +
            '<div class="card-header padding"><a data-toggle="modal" href="' + href + '" target="' + redirect + '" class="padding-bottom-list ' + classattr + '">' + title + '</a></div>' +
            '<div class="card-stat">' +
            '<div class="like-wrapper stat-wrapper">' +
            '<i id="like-icon" class="color-base material-icons icon-mini-article '+liked_attr+'">favorites</i>' +
            '<span id="like-counter" class="counter-wrapper">' + favorite_counter + '</span>' +
            '</div>' +
            '<div class="bigup-wrapper stat-wrapper">' +
            '<i id="bigup-icon" class="color-base material-icons icon-mini-article">thumb_up</i>' +
            '<span id="bigup-counter" class="counter-wrapper">' + useful_counter + '</span>' +
            '</div>' +
            '<div class="view-wrapper stat-wrapper">' +
            '<i id="view-icon" class="color-base material-icons icon-mini-article">visibility</i>' +
            '<span id="view-counter" class="counter-wrapper">' + view_counter + '</span>' +
            '</div>' +
            '</div>' +
            '<div class="tags-mini-article">' +
            'tags' +
            '</div>' +
            '<div class="card-action padding" style="display: none">ACTION</div>' +
            '<div class="card-status">' +
            (essential ? '<i id="" class="color-explicit material-icons">explicit</i>' : '') +
            (newart ? '<i id="" class="color-new material-icons">fiber_new</i>' : '') +
            (nb_attachment > 0 ? '<i id="" class="material-icons att">attachments</i>' : '') +
            '</div>' +
            '</div>';
    };

    var urls = {
        'get_list_articles': GET_LIST_ARTICLES,
        'get_list_daily_recap': GET_DAILY_RECAP,
        'get_polls': GET_POLLS,
        'wrong_or_right': W_O_R,
        'get_popular_tags': GET_POPULAR_TAGS_VIEW
    };

    var selector_action = {
        'att': '.att',
        'color-explicit': '.color-explicit',
        'like_selector': '.favorite',
        'read_selector': '.read-button',
        'bigup_selector': '.useful',
        'comment-to-step-2': '.button-next-step-feedback',
        'comment-to-step-1': '.button-back-step-feedback',
        'comment-step-3': '.button-step3-step-feedback',
        'send-feedback': 'form-feedback',
        'icon-feedback': '.mark',
        'submit-feedback': '.submit-feedback',

        'any_date': '.any_date',
        'today': '.today',
        'past_7_days': '.past_7_days',
        'this_month': '.this_month',
        'this_year': '.this_year',

        'any_date_p': '.any_date_p',
        'today_p': '.today_p',
        'past_7_days_p': '.past_7_days_p',
        'this_month_p': '.this_month_p',
        'this_year_p': '.this_year_p',

        'choice': '.choice',
        'restart-poll': '.restart-poll',
        'show-results-poll': '.show-results-poll',

        // HOME TEMPLATES
        'home': '#home',
        'essentials': '#essentials',
        'most_popular': '#most_popular',
        'new': '#new',

        // DAILY RECAPS TEMPLATE
        'more_daily_recap': '.more_daily_recap',
        'all_daily_recaps': '#all_daily_recaps',
        'last_7_days': '#last_7_days',
        'today_daily_recaps': '#today',
        'unread_daily_recaps': '#unread',
        'read_daily_recaps': '#read',
        'most_view': '#most_view',
        'nextq': '.nextq',

        // SEARCH
        'search_button': '#search'
    };

    var selector = {
        'body_selector': '.modal-body-article',
        'stats_selector': '.modal-stats-article',
        'comment_selector': '.modal-comments-article',
        'attachment_selector': '.modal-attachments-article',
        'like_icon': '.favorite'
    }
};

function design_top_menu(object) {
    $('.top-menu .material-icons').removeAttr('style');
    $('.top-button').removeAttr('style');
    $('.top-menu .txt').removeAttr('style');


    $(object).find('.material-icons').css('color', 'rgb(93, 93, 93)');
    $(object).find('.txt').css('color', 'rgb(93, 93, 93)');
}

function design_top_menu_daily_recaps(object) {
    $('.top-menu-daily-recap .material-icons').removeAttr('style');
    $('.top-button').removeAttr('style');
    $('.top-menu-daily-recap .txt').removeAttr('style');

    $(object).find('.material-icons').css('color', 'rgb(93, 93, 93)');
    $(object).find('.txt').css('color', 'rgb(93, 93, 93)');
}

