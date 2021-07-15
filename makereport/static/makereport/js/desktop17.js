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


//Important Note

//This pen Copyrighted (c) 2016 by Nikhil Krishnan (https://codepen.io/nikhil8krishnan/pen/ALLLkv). If you have any query please let me know at nikhil8krishnan@gmail.com.


//material contact form animation
var floatingField = $('.material-form .floating-field').find('.form-control');
var formItem = $('.material-form .input-block').find('.form-control');

//##case 1 for default style
//on focus

var Upload = function (file, url) {
    this.file = file;
    this.url = url;
};

Upload.prototype.getType = function () {
    return this.file.type;
};
Upload.prototype.getSize = function () {
    return this.file.size;
};
Upload.prototype.getName = function () {
    return this.file.name;
};
Upload.prototype.getUrl = function () {
    return this.url;
}

Upload.prototype.doUpload = function () {
    var that = this;
    var formData = new FormData();

    // add assoc key values, this will be posts values
    formData.append("file", this.file, this.getName());
    formData.append('type', this.file.type);
    formData.append("upload_file", true);

    $.ajax({
        type: "POST",
        beforeSend: function (xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        url: `${this.getUrl()}`,
        xhr: function () {
            var myXhr = $.ajaxSettings.xhr();
            if (myXhr.upload) {
                myXhr.upload.addEventListener('progress', that.progressHandling, false);
            }
            return myXhr;
        },

        success: function (data) {
            // your callback here
        },
        error: function (error) {
            // handle error
        },
        async: true,
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        timeout: 60000
    });
};

Upload.prototype.progressHandling = function (event) {
    var percent = 0;
    var position = event.loaded || event.position;
    var total = event.total;
    var progress_bar_id = "#progress-wrp";
    if (event.lengthComputable) {
        percent = Math.ceil(position / total * 100);
    }
    // update progressbars classes so it fits your code
    $(progress_bar_id + " .progress-bar").css("width", +percent + "%");
    $(progress_bar_id + " .status").text(percent + "%");
};

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
$('#upload').click(function () {
    $("#myFile").click();
});
$('#upload_agreement').click(function () {
    $("#agreementFile").click();
});
$('#upload_mixing').click(function () {
    $("#mixingFile").click();
});
$('#upload_additional').click(function () {
    $("#additionalFile").click();
});
$('#upload_pdf').click(function () {
    $("#mixingPDF").click();
});

function shipOff(name, tag) {
    uploadFile(name, tag, "text/html");
    // var result = document.getElementById(tag).files[0];
    // var upload = new Upload(result, name);
    // var content = upload.getType() === "text/html";
    // if (content) {
    //     upload.doUpload();
    //     alert("Ваш template успешно загружен")
    // } else {
    //     alert("Файл должен быть в xml формате")
    // }
}

function uploadFile(url, tag, formatFile) {
    var result = document.getElementById(tag).files[0];
    var upload = new Upload(result, url);
    var content = upload.getType() === formatFile;
    if (content) {
        upload.doUpload();
        alert("Ваш template успешно загружен")
    } else {
        alert("Файл был загружен в не правильном формате")
    }
}

$(document).ready(function () {
    function processFile(tag) {
        var file = document.getElementById(tag).files[0];
        var reader = new FileReader();
        reader.readAsText(file, 'UTF-8');
    }

    function getFileName(tag, url) {
        return function (elm) {
            processFile(tag);
            uploadFile(`get_template/${url}`, tag, "text/html");
        }
    }

    function uploadPDF(tag, url) {
        return function (elm) {
            processFile(tag);
            uploadFile(url, tag, 'application/pdf')
        }
    }

    $("#myFile").on("change", getFileName('myFile', 'base'));
    $("#mixingFile").on("change", getFileName('mixingFile', 'mixing'));
    $("#agreementFile").on("change", getFileName('agreementFile', 'agreement'));
    $("#additionalFile").on("change", getFileName('additionalFile', 'additional'));
    // $("#mixingPDF").on("change", uploadPDF('mixingPDF', '/mixing_pdf'));
});

//dropdown list
$('body').click(function () {
    if ($('.custom-select .drop-down-list').is(':visible')) {
        $('.custom-select').parent().removeClass('focus');
    }
    $('.custom-select .drop-down-list:visible').slideUp();
});
$('.custom-select .active-list').click(function () {
    $(this).parent().parent().addClass('focus');
    $(this).parent().find('.drop-down-list').stop(true, true).delay(10).slideToggle(300);
});
$('.custom-select .drop-down-list li').click(function () {
    var listParent = $(this).parent().parent();

    listParent.parent('.select-block').removeClass('focus');

});

