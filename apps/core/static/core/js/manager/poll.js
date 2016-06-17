/**
 * Created by maxbook on 02/06/16.
 */

/****************   POLL   ******************/

var Poll = function (id, element) {
    this.element = element;
    this.id = id;
    this.current_number_of_right_choice = 0;
    var current_question = null;

    this.getCurrentQuestion = function (id, current_id) {
        queryCurrentQuestion(id);
        return current_question;
    };

    this.setCurrentQuestion = function (current_id) {
        queryCurrentQuestion(this.id, current_id, 'w');
    };

    var queryCurrentQuestion = function (id, current_id, mode) {
        $.get(GET_CURRENT_QUESTION, {
            'id': id,
            'mode': mode || null,
            'current_id': current_id || null
        }, function (data) {
            if (mode == 'r')
                current_question = data['current_question'];
        })
    };


    // GET POLL JSON FROM DATABASE
    var query = function (id) {
        $.ajax({
            url: urls.show_poll,
            beforeSend: function () {
                $(selector.body_selector).empty().append('<div class="loading mdl-spinner mdl-js-spinner is-active"></div>');
            },
            data: {
                'id': id
            },
            success: function (data) {
                results(data);
            }
        });
    };

    // GET POLL HTML
    var poll = function (poll_id, poll_title, questions) {
        var body = '<div class="body-poll">';
        var header = '<div class="poll" id="' + poll_id + '">' +
            '<div class="header_poll">' +
            '<button type="button" class="close close-poll" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>' +
            '<div class="title_poll">' + poll_title + '</div>' +
            '</div><div class="progress-bar-poll"></div>';
        var counter_question = 0;
        var counter_choice_right = 0;
        for (var question in questions) if (questions.hasOwnProperty(question)) {
            var counter = 0;
            counter_question++;
            var choices = questions[question];
            body += '<div class="question-poll" id="question' + counter_question + '">' +
                '<div class="img_poll"><img style="display: none;" src="#"></div>' +
                '<div class="title-question">' + question + '</div><div class="choices">';
            for (var choice in choices) if (choices.hasOwnProperty(choice)) {
                counter++;
                if (choices[choice]['type'] == 0) {
                    counter_choice_right++;
                }
                body += '<div id="' + choices[choice]['choice_id'] + '" class="wc' + choices[choice]['type']
                    + '' +
                    ' choice ' + counter + '">' + choices[choice]['choice_title'] + '</div>';
            }
            body += '</div></div>';
        }
        body += '</div>';
        var footer = '<footer><button id="" class="nextq">' +
            'Next > ' +
            '</button><span class="nb_questions" id="' + counter_question + '" style="display: none"></span>' +
            '<span class="nb_choice_right" id="' + counter_choice_right + '" style="display: none"></span></div></footer>';

        return header + body + footer;
    };

    // APPEND POLL HTML
    var results = function (data, display) {
        var result = '';
        for (var key in data) if (data.hasOwnProperty(key)) {
            var questions = data[key]['questions'];
            result = poll(key, data[key]['poll_title'], questions);
        }
        $(selector.body_selector).empty().append(result);
        $('.body-poll').children('div:not(#question1)').hide();
        initColors(window.Manager.getPrimaryColor(), window.Manager.getSecondaryColor(), window.Manager.getImgUrl());
    };

    // SHOW POLL
    this.show = function () {
        query(this.id);
    };


    var selector = {
        'body_selector': '.modal-body-poll'
    };

    var urls = {
        'show_poll': SHOW_POLL
    };


    // this.isComplete = function () {
    //     return query(urls.read_manager, mode.read);
    // };
    //
    // this.setComplete = function (active, inactive) {
    //     query(urls.like_manager, mode.write);
    //     query_action(this.id, true, urls.read_manager);
    //     design(this.read_selector, this.isRead(), active, inactive);
    // };
    //
    // var query_action = function (id, bool, url) {
    //     $.get(url,
    //         {'id': id, 'action': bool},
    //         function (data) {
    //
    //         }
    //     );
    // };
    //
    // var design = function (element, state, object, active, inactive) {
    //     switch (element) {
    //         case selector.bigup_icon:
    //             if (state) {
    //                 object.attr('class', active || attrclass.bigup);
    //                 object.text(parseInt(object.text()) + 1);
    //             }
    //             else {
    //                 object.attr('class', inactive || attrclass.unbigup);
    //                 object.text(parseInt(object.text()) - 1);
    //             }
    //             break;
    //         default:
    //             break;
    //     }
    // };

    function loadScript(url, callback) {
        var docHeadObj = document.getElementsByTagName("head")[0];
        var dynamicScript = document.createElement("script");
        dynamicScript.type = "text/javascript";
        dynamicScript.src = url;

        // bind the event to the callback function
        dynamicScript.onreadystatechange = callback; //for ie<9
        dynamicScript.onload = callback;

        // Fire the loading
        docHeadObj.appendChild(dynamicScript);
    }


    var testJQuery = function () {
    };
};