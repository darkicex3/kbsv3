/**
 * Created by maxbook on 02/06/16.
 */

/****************      RENDER    ******************/

function resize_masterfeed() {
    var margin = 11;
    var leftbarwidth = $('.left-sidebar').width() + margin * 2;
    var rightbarwidth = $('.right-sidebar').width() + margin * 2;
    var windowwidth = $(window).width();

    $('.master-feed').css('width', windowwidth - (leftbarwidth + rightbarwidth));
    $('.table-article').css('width', windowwidth - (leftbarwidth + rightbarwidth)).css('resize', 'both').css('overflow', 'auto');
}

function resize_sidebars() {
    var windowwidth = $(window).width();
    var masterfeed = $('.master-feed').width();
    var sidebar = $('.left-sidebar').width();

    var size = ((windowwidth - (masterfeed + sidebar + 71)));

    $('.right-sidebar').css('width', size);
}

function resize_module() {
    var headerheight = $('header').height();
    var windowheight = $(window).height();
    var rightbarheight = (windowheight - headerheight) - 10;
    var moduleheight = ( rightbarheight / 3 ) - 10;

    $('.right-sidebar').css('height', rightbarheight);
    $('.module').css('height', moduleheight - 15);
}

function render_article() {
    var article_content = $('.modal-content-article');
    var article = $('.article');
    var counter = 0;
    var glossary = '<div class="glossary-header">Glossary<i class="material-icons">library_books</i></div><a class="link-glossary top-article">Header</a>';
    var current_title = '';

    $('.content-article').find('*').each(function () {
        $(this).removeAttr('style');
    });

    article_content.find('*').each(function () {
        var element = $(this);

        if (element.width() > element.parent().width()) {
            element.css('width', '100%').css('height', 'auto');
        }

        if (((element.prev().is('p') || element.prev().is('div')) && (element.prev().html() == '<br>' || element.html() == '<br />'))
            && ((element.is('p') || element.is('div')) && (element.html() == '<br>' || element.html() == '<br />'))) {
            element.remove();
        }

        if ((element.prev().is('h1') || element.prev().is('h2') || element.prev().is('h3') || element.prev().is('h4')
            || element.prev().is('h5') || element.prev().is('h6')) && ((element.html() == '<br>') && (element.is('p') || element.is('div')))) {
            element.remove();
        }

        if (element.is('h1') || element.is('h2') || element.is('h3') || element.is('h4')
            || element.is('h5') || element.is('h6')) {

            counter += 1;
            element.attr('id', 'title' + counter);
            glossary += '<a class="link-glossary" href="#' + 'title' + counter + '">' + element.text() + '</a>';
        }
    });

    glossary += '<a class="bottom-article">Something to say ?</a>';

    $('.modal-glossary-article').empty().append(glossary);
    position_module_article();

    $('.link-glossary').click(function () {
        var scroll_elem = $('.modal-dialog-article');
        if ($(this).attr('class') == 'link-glossary top-article') {
            scroll_elem.animate({
                scrollTop: 0
            }, 300);
        } else {
            scroll_elem.animate({
                scrollTop: $($.attr(this, 'href')).offset().top + scroll_elem.scrollTop() - 20
            }, 300);
        }
    });

    $('.bottom-article').click(function () {
        var scroll_elem = $('.modal-dialog-article');
        scroll_elem.animate({
            scrollTop: $('.modal-content-article').height() + scroll_elem.scrollTop()
        }, 300);
    });


    var min_height = $(window).height() - 30;
    article_content.css('min-height', min_height);

}

function position_module_article() {
    var pos = $('.modal-dialog-article').width();
    var bodywidth = $(window).width();
    var right = ((bodywidth - pos) / 2 ) - 210;
    var left = ((bodywidth - pos) / 2 ) - 68;


    $('.modal-glossary-article').css('right', right);
    $('.float-menu-left').css('left', left);
}

function resize_iframe() {
    var elem = $('.content-article');
    elem.find('iframe').attr('width', '100%').removeAttr('style').parent().removeAttr('style');
}

function reposition_stat_glossary() {
    var pos = $('.modal-dialog-article').width();
    var bodywidth = $(window).width();
    var right = ((bodywidth - pos) / 2 ) - 210;
    var left = ((bodywidth - pos) / 2 ) - 90;

    $('.modal-glossary-article').css('right', right);
    $('.float-menu-left').css('left', left);
}

function renderPDFfromUrl(url) {
    PDFJS.getDocument(url)
        .then(function (pdf) {

            // Get div#the-svg
            var container = document.getElementById('svg-rendering');

            // Loop from 1 to total_number_of_pages in PDF document
            for (var i = 1; i <= pdf.numPages; i++) {

                // Get desired page
                pdf.getPage(i).then(function (page) {

                    // Set scale (zoom) level
                    var scale = 1;

                    // Get viewport (dimensions)
                    var viewport = page.getViewport(scale);

                    // SVG rendering by PDF.js
                    page.getOperatorList()
                        .then(function (opList) {
                            var svgGfx = new PDFJS.SVGGraphics(page.commonObjs, page.objs);
                            return svgGfx.getSVG(opList, viewport);
                        })
                        .then(function (svg) {
                            svg.setAttribute('style', 'width:100%;');
                            container.appendChild(svg);
                        });
                });
            }
        });
}
