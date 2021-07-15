// a can just change url and everything will work as expected. But I will give some time to make up better ideas
$('#sign').on('click', function () {
    loadModels($(this))
})
$('#sign_boss').on('click', function () {
    loadModels($(this))
})
var sign_user;
var url = "https://e-otsenka.uz/report/ajax/verifyPkcs7/";
function success_sign() {
    console.log(typeof (sign_user));
    if (sign_user === '0') {
        $("#company_sign").css('display','none');
    }
    else {
         $("#user_sign").css('display','none');
    }
}
function loadModels(object) {
    let sign = object.attr('sign');
    let sign_form = object.attr('sign_from')
        var model = $("#exampleModal");
    model.modal('show');
    sign_user = sign_form;
    model.find('.sign').val(sign)
    model.find('.sign_form').val(sign_form)
    let recipient = object.attr('data-bs-whatever');
    let report_id = object.attr('data-bs-report');
    var modalFileInput = model.find('.file');
    var modalReportIdField = model.find('.report_id');
    modalFileInput.text(recipient)
    modalReportIdField.val(report_id)

}

$('#close_model').on('click', function () {
    $("#exampleModal").modal('hide');
})
$('#close_m').on('click', function () {
    $("#exampleModal").modal('hide');
})
// var exampleModal = document.getElementById('exampleModal')
// exampleModal.addEventListener('show.bs.modal', function (event) {
//     var button = event.relatedTarget;
//     var recipient = "";
//     var sign = button.getAttribute('sign');
//     var sign_from = button.getAttribute('sign_from');
//     exampleModal.querySelector('.sign').value = sign;
//     exampleModal.querySelector('#sign_from').value = sign_from;
//
//     recipient = button.getAttribute('data-bs-whatever');
//     var report_id = button.getAttribute('data-bs-report');
//
//     var modalFileInput = exampleModal.querySelector('.file');
//     var modalReportIdField = exampleModal.querySelector('.report_id');
//
//     modalFileInput.textContent = recipient
//     modalReportIdField.value = report_id
// })

// $('#exampleModal').on('hidden.bs.modal', function (e) {
//     location.reload();
// })

$(document).on('click', ".btn btn-primary sign", function (e) {
    console.log('CLICK sign')
    var pkcs7 = $(this).parents('.modal-body').find('.pkcs7').textContent;
    console.log(pkcs7)
});

var EIMZO_MAJOR = 3;
var EIMZO_MINOR = 37;


var errorCAPIWS = 'Ошибка соединения с E-IMZO. Возможно у вас не установлен модуль E-IMZO или Браузер E-IMZO.';
var errorBrowserWS = 'Браузер не поддерживает технологию WebSocket. Установите последнюю версию браузера.';
var errorUpdateApp = 'ВНИМАНИЕ !!! Установите новую версию приложения E-IMZO или Браузера E-IMZO.<br /><a href="https://e-imzo.uz/main/downloads/" role="button">Скачать ПО E-IMZO</a>';
var errorWrongPassword = 'Пароль неверный.';


var AppLoad = function () {
    EIMZOClient.API_KEYS = [
        'localhost', '96D0C1491615C82B9A54D9989779DF825B690748224C2B04F500F370D51827CE2644D8D4A82C18184D73AB8530BB8ED537269603F61DB0D03D2104ABF789970B',
        '127.0.0.1', 'A7BCFA5D490B351BE0754130DF03A068F855DB4333D43921125B9CF2670EF6A40370C646B90401955E1F7BC9CDBF59CE0B2C5467D820BE189C845D0B79CFC96F',
        'null', 'E0A205EC4E7B78BBB56AFF83A733A1BB9FD39D562E67978CC5E7D73B0951DB1954595A20672A63332535E13CC6EC1E1FC8857BB09E0855D7E76E411B6FA16E9D',
        'dls.yt.uz', 'EDC1D4AB5B02066FB3FEB9382DE6A7F8CBD095E46474B07568BC44C8DAE27B3893E75B79280EA82A38AD42D10EA0D600E6CE7E89D1629221E4363E2D78650516'
    ];
    uiLoading();
    EIMZOClient.checkVersion(function (major, minor) {
        var newVersion = EIMZO_MAJOR * 100 + EIMZO_MINOR;
        var installedVersion = parseInt(major) * 100 + parseInt(minor);
        if (installedVersion < newVersion) {
            uiUpdateApp();
        } else {
            EIMZOClient.installApiKeys(function () {
                uiLoadKeys();
            }, function (e, r) {
                if (r) {
                    uiShowMessage(r);
                } else {
                    wsError(e);
                }
            });
        }
    }, function (e, r) {
        if (r) {
            uiShowMessage(r);
        } else {
            uiNotLoaded(e);
        }
    });
}


var uiShowMessage = function (message) {
    alert(message);
}

var uiLoading = function () {
    var l = document.getElementById('message');
    l.innerHTML = 'Загрузка ...';
    l.style.color = 'red';
}

var uiNotLoaded = function (e) {
    var l = document.getElementById('message');
    l.innerHTML = '';
    if (e) {
        wsError(e);
    } else {
        uiShowMessage(errorBrowserWS);
    }
}

var uiUpdateApp = function () {
    var l = document.getElementById('message');
    l.innerHTML = errorUpdateApp;
}

var uiLoadKeys = function () {
    uiClearCombo();
    EIMZOClient.listAllUserKeys(function (o, i) {
        var itemId = "itm-" + o.serialNumber + "-" + i;
        return itemId;
    }, function (itemId, v) {
        return uiCreateItem(itemId, v);
    }, function (items, firstId) {
        uiFillCombo(items);
        uiLoaded();
        uiComboSelect(firstId);
    }, function (e, r) {
        uiShowMessage(errorCAPIWS);
    });
}

var uiComboSelect = function (itm) {
    if (itm) {
        var id = document.getElementById(itm);
        id.setAttribute('selected', 'true');
    }
}

var cbChanged = function (c) {
    document.getElementById('keyId').innerHTML = '';
}

var uiClearCombo = function () {
    var combo = document.testform.key;
    combo.length = 0;
}

var uiFillCombo = function (items) {
    var combo = document.testform.key;
    for (var itm in items) {
        combo.append(items[itm]);
    }
}

var uiLoaded = function () {
    var l = document.getElementById('message');
    l.innerHTML = '';
}

var uiCreateItem = function (itmkey, vo) {
    var now = new Date();
    vo.expired = dates.compare(now, vo.validTo) > 0;
    var itm = document.createElement("option");
    itm.value = itmkey;
    itm.text = vo.CN;
    if (!vo.expired) {

    } else {
        itm.style.color = 'gray';
        itm.text = itm.text + ' (срок истек)';
    }
    itm.setAttribute('vo', JSON.stringify(vo));
    itm.setAttribute('id', itmkey);
    return itm;
}

var wsError = function (e) {
    if (e) {
        uiShowMessage(errorCAPIWS + " : " + e);
    } else {
        uiShowMessage(errorBrowserWS);
    }
};

verify = function () {
    var pkcs7 = document.testform.pkcs7.value;
    EIMZOClient.verifyPkcs7(pkcs7,)
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
sign_decide = function (obj) {
    var model = $("#sign_boss");

    var choice = document.getElementById("sign").value;
    console.log('sign decide')
     console.log(sign_user);
    sign();

}
adding_sign = function () {
    var sign_from = document.getElementById('sign_from');

    var itm = document.testform.key.value;
    if (itm) {
        var id = document.getElementById(itm);
        var vo = JSON.parse(id.getAttribute('vo'));
        var data = document.testform.data.value;
        var keyId = document.getElementById('keyId').innerHTML;
        var report_input = document.getElementById('report_id');
        var sign_from = document.getElementById('sign_from');
        var pkcs7 = document.getElementsByClassName('file');
        console.log("in");
        console.log(keyId);
        if (keyId) {
            EIMZOClient.append_pkcs7_attached(keyId, pkcs7, null, function (pkcs7) {

                console.log("SUCESSS")
                console.log("ADDDEDDD")
                console.log('s')
                $.ajax({
                    type: "POST",
                    headers: {
                        "X-CSRFToken": csrftoken
                    },
                    url: url,
                    data: {
                        'pkcs7': pkcs7,
                        'sign_from': sign_from.value,
                        'report_id': report_input.value,

                    },
                    cache: true,
                    success: function (data) {
                        alert("Ваша подпись была успешна добавлена!")
                    },
                    error: function (xhr, ajaxOptions, thrownError) {
                        alert(xhr.status);
                        alert(thrownError);
                    }
                })
            }, function (e, r) {
                if (r) {
                    if (r.indexOf("BadPaddingException") != -1) {
                        uiShowMessage(errorWrongPassword);
                    } else {
                        uiShowMessage(r);
                    }
                } else {
                    document.getElementById('keyId').innerHTML = '';
                    console.log(e)
                    uiShowMessage(errorBrowserWS);
                }
                if (e) wsError(e);
            });
        } else {
            EIMZOClient.loadKey(vo, function (id) {
                document.getElementById('keyId').innerHTML = id;
                EIMZOClient.createPkcs7(id, data, null, function (pkcs7) {
                    document.testform.pkcs7.value = pkcs7;
                }, function (e, r) {
                    if (r) {
                        if (r.indexOf("BadPaddingException") != -1) {
                            uiShowMessage(errorWrongPassword);
                        } else {
                            uiShowMessage(r);
                        }
                    } else {
                        document.getElementById('keyId').innerHTML = '';
                        uiShowMessage(errorBrowserWS);
                    }
                    if (e) wsError(e);
                    console.log(e)
                });
            }, function (e, r) {
                if (r) {
                    if (r.indexOf("BadPaddingException") != -1) {
                        uiShowMessage(errorWrongPassword);
                    } else {
                        uiShowMessage(r);
                    }
                } else {
                    uiShowMessage(errorBrowserWS);
                }
                if (e) wsError(e);

            });
        }
    }
}
sign = function () {
    var sign_from = document.getElementById('sign_from');
     var report_input = document.getElementById('report_id');
    console.log(sign_from.value);
    console.log("sadsdsdasd");
    var itm = document.testform.key.value;
    if (itm) {
        var id = document.getElementById(itm);
        var vo = JSON.parse(id.getAttribute('vo'));
        var data = document.testform.data.value;
        var keyId = document.getElementById('keyId').innerHTML;
        var report_input = document.getElementById('report_id');
        if (keyId) {
            EIMZOClient.createPkcs7(keyId, data, null, function (pkcs7) {

                $.ajax({
                    type: "POST",
                    headers: {
                        "X-CSRFToken": csrftoken
                    },
                    url: url,
                    data: {
                        'pkcs7': pkcs7,
                        'sign_from': sign_user,
                        'report_id': report_input.value,

                    },
                    cache: true,
                    success: function (data) {
                        success_sign();
                        alert("Вы успешно подписали документ!");
                    },
                })
            }, function (e, r) {
                if (r) {
                    if (r.indexOf("BadPaddingException") != -1) {
                        uiShowMessage(errorWrongPassword);
                    } else {
                        uiShowMessage(r);
                    }
                } else {
                    document.getElementById('keyId').innerHTML = '';
                    uiShowMessage(errorBrowserWS);
                }
                if (e) wsError(e);
            });
        } else {
            EIMZOClient.loadKey(vo, function (id) {
                document.getElementById('keyId').innerHTML = id;
                EIMZOClient.createPkcs7(id, data, null, function (pkcs7) {
                    document.testform.pkcs7.value = pkcs7;
                }, function (e, r) {
                    if (r) {
                        if (r.indexOf("BadPaddingException") != -1) {
                            uiShowMessage(errorWrongPassword);
                        } else {
                            uiShowMessage(r);
                        }
                    } else {
                        document.getElementById('keyId').innerHTML = '';
                        uiShowMessage(errorBrowserWS);
                    }
                    if (e) wsError(e);
                });
            }, function (e, r) {
                if (r) {
                    if (r.indexOf("BadPaddingException") != -1) {
                        uiShowMessage(errorWrongPassword);
                    } else {
                        uiShowMessage(r);
                    }
                } else {
                    uiShowMessage(errorBrowserWS);
                }
                if (e) wsError(e);
            });
        }
    }
};

window.onload = AppLoad;
