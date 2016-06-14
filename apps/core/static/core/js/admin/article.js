/**
 * Created by maxbook on 31/05/16.
 */

(function ($) {
    $(function () {

        var is_public = $('#id_is_public');
        var by_groups = $('#id_by_groups');
        var file_content_option = $('#id_file_content_option');
        var url_content_option = $('#id_url_content_option');

        if (file_content_option.is(':checked')) {
            showFileOption();
        } else {
            hideFileOption();
        }

        if (url_content_option.is(':checked')) {
            showUrlOption();
        } else {
            hideUrlOption();
        }

        if (is_public.is(':checked')) {
            hideAllAdvanced();
        } else if (!is_public.is(':checked') && !by_groups.is(':checked')) {
            hideByGroups();
        }

        is_public.click(function () {
            if ($(this).is(':checked')) {
                hideAllAdvanced();
            } else if (!$(this).is(':checked')) {
                showByGroups();
            }
        });

        by_groups.click(function () {
            if ($(this).is(':checked')) {
                showByGroups();
                hideByUsers();
            } else if (!$(this).is(':checked')) {
                showByUsers();
                hideByGroups();
            }
        });

        file_content_option.click(function () {
            if ($(this).is(':checked')) {
                showFileOption();
                hideUrlOption();
            } else if (!$(this).is(':checked')) {
                hideFileOption();
            }
        });

        url_content_option.click(function () {
            if ($(this).is(':checked')) {
                showUrlOption();
                hideFileOption();
            } else if (!$(this).is(':checked')) {
                hideUrlOption();
            }
        });


        // FUNCTIONS SHOW HIDE DIV ARTICLE ADMIN
        function showUrlOption() {
            file_content_option.prop('checked', false);
            $('.field-url_article').slideDown(200)
        }

        function hideUrlOption() {
            $('.field-url_article').slideUp(200)
        }

        function showFileOption() {
            url_content_option.prop('checked', false);
            $('.field-file_content').slideDown(200)
        }

        function hideFileOption() {
            $('.field-file_content').slideUp(200)
        }

        function hideAllAdvanced() {
            $('.field-by_groups').slideUp(200);
            $('.field-authorized_groups').slideUp(200);
            $('.field-authorized_users').slideUp(200);
            $('.field-authorized_users_dr').slideUp(200);
        }

        function hideByGroups() {
            $('.field-authorized_groups').slideUp(200);
        }

        function showByGroups() {
            $('#id_by_groups').prop('checked', true);
            $('.field-by_groups').slideDown(200);
            $('.field-authorized_groups').slideDown(200);
        }

        function hideByUsers() {
            $('.field-authorized_users').slideUp(200);
            $('.field-authorized_users_dr').slideUp(200);
        }

        function showByUsers() {
            $('.field-authorized_users').slideDown(200);
            $('.field-authorized_users_dr').slideDown(200);
        }
    });
})(django.jQuery);
