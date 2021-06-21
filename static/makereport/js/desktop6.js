/**
 * Template Name: iPortfolio - v1.4.1
 * Template URL: https://bootstrapmade.com/iportfolio-bootstrap-portfolio-websites-template/
 * Author: BootstrapMade.com
 * License: https://bootstrapmade.com/license/
 */
!(function ($) {
    "use strict";


    $(document).on('click', '.mobile-nav-toggle', function (e) {
        $('body').toggleClass('mobile-nav-active');
        $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
    });

    $(document).click(function (e) {
        var container = $(".mobile-nav-toggle");
        if (!container.is(e.target) && container.has(e.target).length === 0) {
            if ($('body').hasClass('mobile-nav-active')) {
                $('body').removeClass('mobile-nav-active');
                $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
            }
        }
    });


})(jQuery);


$('.dropdown-el').click(function (e) {
    e.preventDefault();
    e.stopPropagation();
    $(this).toggleClass('expanded');
    $('#' + $(e.target).attr('for')).prop('checked', true);
});
$(document).click(function () {
    $('.dropdown-el').removeClass('expanded');
});


$('.dropdown-el1').click(function (e) {
    e.preventDefault();
    e.stopPropagation();
    $(this).toggleClass('expanded');
    $('#' + $(e.target).attr('for')).prop('checked', true);
});
$(document).click(function () {
    $('.dropdown-el1').removeClass('expanded');
});
//Important Note

//This pen Copyrighted (c) 2016 by Nikhil Krishnan (https://codepen.io/nikhil8krishnan/pen/ALLLkv). If you have any query please let me know at nikhil8krishnan@gmail.com.


//material contact form animation
var floatingField = $('.material-form .floating-field').find('.form-control');
var formItem = $('.material-form .input-block').find('.form-control');

//##case 1 for default style
//on focus
formItem.focus(function () {
    $(this).parent('.input-block').addClass('focus');
});
//removing focusing
formItem.blur(function () {
    $(this).parent('.input-block').removeClass('focus');
});

//##case 2 for floating style
//initiating field
floatingField.each(function () {
    var targetItem = $(this).parent();
    if ($(this).val()) {
        $(targetItem).addClass('has-value');
    }
});

//on typing
floatingField.blur(function () {
    $(this).parent('.input-block').removeClass('focus');
    //if value is not exists
    if ($(this).val().length == 0) {
        $(this).parent('.input-block').removeClass('has-value');
    } else {
        $(this).parent('.input-block').addClass('has-value');
    }
});

//dropdown list
$('body').click(function () {
    // if ($('.custom-select .drop-down-list').is(':visible')) {
    //     $('.custom-select').parent().removeClass('focus');
    // }
    // $('.custom-select .drop-down-list:visible').slideUp();
});
$('.custom-select .active-list').click(function () {
    // $(this).parent().parent().addClass('focus');
    $(this).parent().find('.drop-down-list').stop(true, true).delay(10).slideToggle(300);
});

$('#page_list li').click(function () {
    $("#page_input").attr('value', $(this).attr('id_attr'))
    $("#page_form").submit();
})
$('#sign_list li').click(function () {
    $("#sign_input").attr('value', $(this).attr('id_attr'))
    $("#sign_form").submit();
})