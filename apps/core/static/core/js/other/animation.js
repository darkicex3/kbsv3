/**
 * Created by maxbook on 27/04/16.
 */

// function OnMouseEnterMouseLeaveTags() {
//     $('body').on({
//         mouseenter: function () {
//             if ($('#search_bar input[name=\'csrfmiddlewaretoken\']').attr('value') != getCookie('csrftoken')) {
//                 var width = ($(this).width() / 2) - 9;
//                 $(this).find('.add-tags').css({'left': width}).show(100);
//             }
//         },
//         mouseleave: function () {
//             $(this).find('.add-tags').hide();
//         }
//     }, '.bookmarkBadge');
// }

function OnAttachment() {
    function rotate(elem, degree) {

        elem.css({ WebkitTransform: 'rotate(' + degree + 'deg)'});
        elem.css({ '-moz-transform': 'rotate(' + degree + 'deg)'});
        var timer = setTimeout(function() {
            ++degree; rotate();
        },5);
    }

    var button = $('.attachment-button');
    $('body').on({
        mouseenter: function () {
            var elem = $('.attachment-article');
            if (elem.html() != '')
                elem.stop().slideDown(300);
        },
        mouseleave: function () {
            var elem = $('.attachment-article');
            if (elem.html() != '')
                elem.stop().slideUp(300);
        }
    }, '.attachment-section');
}

function OnClickBookmarkGetArticlesByBookmark() {
    $('body').on('click', '.bookmarkLink', function (e) {
        $('.top-menu').flip(true);

        var cleaner = $('.clear-search-bar');

        cleaner.children().first().css('color', '#5d5d5d');
        if (!cleaner.is(":visible")) {
            cleaner.show().transition({width: '50px'});
        }



        $('#search_bar input').attr('placeholder', '').empty().css('font-size', '14pt').css('color', '#5d5d5d !important').val('#' + $(this).text());
        $('#search_categories').empty().css('background', '#3498db');
        $('#search_sorting').css('background', '#3498db').find('.sorting').attr('class', 'sorting material-icons color_white md-36 first-item');
        increment_tag_counter($(this).attr('id').slice(1));

        window.Manager.getListArticle($(this).attr('id'));
    });
}

function OnLoadResizeCsb() {
    var csb_width = $('#search_bar').width() / 2;
    $('.clear-search-bar').css('width', csb_width);
}

function OnSearchBar() {
    var cleaner = $('.clear-search-bar');
    var sc = $('#search_categories');
    $('#search_field').click(function () {
        cleaner = $('.clear-search-bar');
        sc = $('#search_categories');
        if (($(this).val() != '' || sc.css('background-color') == 'rgb(52, 152, 219)') && !cleaner.is(":visible"))
            cleaner.show().transition({width: '50px'});
    }).keyup(function () {
        cleaner = $('.clear-search-bar');
        sc = $('#search_categories');
        if ($(this).val() == '' && cleaner.is(":visible")) {
            if (sc.css('background-color') != 'rgb(52, 152, 219)') {
                cleaner.transition({width: '0'}, function () {
                    $(this).hide();
                });
            }
        }
        else if (($(this).val() != '' || sc.css('background-color') == 'rgb(52, 152, 219)') && !cleaner.is(":visible")) {
            cleaner.show().transition({width: '50px'});
        }
    });

    cleaner.click(function () {
        var cat_button = $('#search_categories');
        var cat_content = '<i class="material-icons color_base md-36 first-item">more_horiz</i>';
        var cat_txt = 'more_horiz';
        var sort_button = $('#search_sorting');

        $(this).children().first().css('color', '#5F5F5F');
        if (cat_button.text() != cat_txt) {
            cat_button.empty().append(cat_content);
            cat_button.css('background', '#fff');
            sort_button.removeAttr('style').find('.sorting').attr('class', 'sorting material-icons color_base md-36 first-item');
        }

        $('#search_field').val('').removeAttr('style').attr('placeholder', 'What are you looking for ?');
        $('.clear-search-bar').transition({width: '0'}, function () {
            $(this).hide();
        });

        window.Manager.getListArticle();
    });
}

function OnClickSearchBarSetEditable() {
    $('body').on('click', '#search_bar input', function (e) {
        var cleaner = $('.clear-search-bar');
        if ($(this).css('background-color') == 'rgb(52, 152, 219)') {
            cleaner.children().first().css('color', '#5F5F5F');
            var value = $(this).val();
            $(this).val('').removeAttr('style');
            $('#search_bar input[name=\'csrfmiddlewaretoken\']').attr('value', getCookie('csrftoken'));
            $('#search_categories').empty().append(value).css({'color': 'white', 'font-size': '12pt'});
            $('#search_sorting').removeAttr('style').find('.sorting').attr('class', 'sorting material-icons color_base md-36 first-item');
            $(this).attr('placeholder', 'What are you looking for ?');
        } else {
            $(this).css('background', '#f3f3f3');
        }
    });
}

function increment_tag_counter(tag_name) {
    $.get(TAGS_COUNTER_INCREMENT, {'in':tag_name}, function (data) {

    });
}

function resize_left_menu() {
    var hbar = $('.left-sidebar').height();
    var hman = $('.copyright').height() + 100;
    var hres = hbar - hman;
    $('.menu-left-menu-container').css('height', hres);
}

function style_choice(choice) {
    if (choice.attr('class').indexOf('active') >= 0)
        choice.removeClass('active-choice');
    else
        choice.addClass('active-choice');
}

function on_mouseover_li_show_children() {
    var nav_wrapper = $('.nav-wrapper');

    if (!window.is_mobile) {
        $('body').on({
            mouseenter: function (event) {
                if ($(this).children('.children').children('li').length > 0) {
                    event.stopPropagation();
                    nav_wrapper.css('width', '468px');
                    $('.ps-scrollbar-y-rail').hide();
                    $('.ps-scrollbar-y').hide();
                    $(this).css('background', '#5d5d5d').children('.children').css('left', '234px').css('display', 'block');

                }
            },
            mouseleave: function (event) {
                event.stopPropagation();
                nav_wrapper.removeAttr('style').show();
                $(this).removeAttr('style').children('.children').css('left', '0').css('display', 'none');
            }
        }, '#variable-menu > li');
    }
}




















