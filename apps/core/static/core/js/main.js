jQuery(document).ready(function ($) {

    window.Manager = new ArticleManager();
    window.body = $('body');
    resize_left_menu();
    resize_sidebars();
    design_top_menu('#home');

    window.is_mobile = ($('.front').css('flex-direction') == 'column');
    console.log($('.front').css('flex-direction'));
    window.nb_polls_displayed = 4;
    window.nb_dr_displayed = 4;
    window.Manager.initEvents();
    window.Manager.getListArticle(); //category, tags, sorting, counter
    window.Manager.getListDailyRecap(null, null, window.nb_dr_displayed);
    window.Manager.getListPolls(null, null, window.nb_polls_displayed);
    window.Manager.getPopularTags();
    window.Manager.setColorKB('rgb(71, 66, 244)');
    initColors(window.Manager.getPrimaryColor(), window.Manager.getSecondaryColor(), window.Manager.getImgUrl());


    $('.top-menu').flip({
        axis: 'x',
        trigger: 'manual',
        speed: '250'
    });

    $('.settings-header').webuiPopover({title: 'Title', content: 'Content', animation: 'pop'});



    $('#search').click(function () {
        $('.top-menu').flip(true);
        $('.modules').css('flex-direction', 'column-reverse');
        window.Manager.getSearchSuggestions();
    });

    $('#display-poll').on('hide.bs.modal', function (e) {
        var poll = new Poll($(this).find('.poll').attr('id')), counter = 0, counter_question = 0;
        $(this).find('.body-poll').find('.question-poll').each(function () {
            counter_question++;
            if ($(this).attr('style') != 'display: none;') {
                counter++;
                poll.setCurrentQuestion($(this).attr('id').replace('question', '') - 1);
            }
        });

        if (counter == 0)
            poll.setCurrentQuestion(counter_question);

        window.Manager.getListPolls(null, null, window.nb_polls_displayed);
    });

    $('#back_search').click(function () {
        $('.top-menu').flip(false);
         $('.modules').removeAttr('style');
    });

    $('.menu-icon').click(function () {
        window.nav_wrapper = $('.nav-wrapper');
        window.app = $('.app');

        console.log(window.is_mobile, 'erwjbjubw : ', $('.main-content').css('padding'));
        if (window.is_mobile) {
            if (window.nav_wrapper.is(':visible'))
                window.nav_wrapper.hide();
            else
                window.nav_wrapper.show();
        }
        else {
            if (window.nav_wrapper.css('left') == '0px') {
                window.nav_wrapper.css('left', window.nav_wrapper.width() * (-1));
                window.app.css('padding-right', '5%').css('padding-left', '5%');
            }
            else {
            window.app.removeAttr('style');
            window.nav_wrapper.css('left', '0');
            }
        }

    });


    $('.nav-wrapper').perfectScrollbar();

    // OnMouseEnterMouseLeaveTags();
    OnClickBookmarkGetArticlesByBookmark();
    OnClickSearchBarSetEditable();
    OnSearchBar();
    OnAttachment();
    on_mouseover_li_show_children();

    window.body.on('click', '.guideText', function (e) {
       window.Manager.getListArticle($(this).attr('id'));
    });

    var nav = $('.menu-button').find('.txt');
    nav.click(function () {
        window.Manager.getListArticle($(this).children('.cat-header').attr('id'));
    });

    $('.category-link').click(function () {

        var selector = $(this).parent().children('.children');
        if (window.is_mobile) {
            if (selector.children('li').length > 0 && !$(this).hasClass('mobile-selected')) {
                $(this).parent().children('.children').css('display', 'block');
                $(this).addClass('mobile-selected');
            }
            else if (selector.children('li').length > 0 && $(this).hasClass('mobile-selected')) {
                $(this).parent().children('.children').css('display', 'none');
                $(this).removeClass('mobile-selected');
            } else if (selector.children('li').length == 0) {
                $('.nav-wrapper').hide();
            }
        }

        if (selector.children('li').length == 0) {

        }

        window.Manager.getListArticle($(this).attr('id'));
        $('.category-link').removeAttr('style');
        $(this).css('color', 'white');

        var child = $(this);
        var txt = '';

        txt = '<span class="cat-header" id="' + child.attr('id') + '">' + child.attr('id') + '</span>';
        nav.empty().html(txt);
    });

    window.body.on('click', '.feedback', function (e) {
        read($(this), READ_MANAGER);
    });

    $(window).resize(function (e) {
        resize_left_menu();
        resize_sidebars();
        position_module_article();
    });

    $('#Home').css('color', 'white');
});