# import qrcode
import requests
import json
from django.http import JsonResponse
from django.core.files.storage import default_storage
from .models import *


def qr_code(signature, valid_from):
    # str_for_qr_code = "success: {success}\nsignature:{signature}\nsignAlgName:{signAlgName}\nlink:{link}\n".format(
    #     success=success, signature=signature, signAlgName=signAlgName, link=link)
    str_for_qr_code = "signature:{signature}           from: {valid_from}".format(
        signature=signature, valid_from=valid_from)
    print(str_for_qr_code)
    return str_for_qr_code
    # img = qrcode.make(str_for_qr_code)  # вот сюда любую ссылку вставите он переведет в QR CODE
    # # Create and save the svg file naming "myqr.svg"
    # img.save('qrcode_test.png')


def serializing(formatted_output):
    check = False
    new_str = ""
    for element in range(len(formatted_output)):
        if formatted_output[element] == "<":
            check = True
        if not check:
            new_str = new_str + formatted_output[element]
        if formatted_output[element] == ">":
            check = False
    return new_str


def get_verifyPkcs7(report_id, sign_from=None):
    data = {}
    print("REPORT ID : ".format(report_id))
    report = Report.objects.get(report_id=report_id)
    pkcs7 = report.pdf_report_pkcs7
    print("PKCS7 : ".format(pkcs7))
    url = "http://127.0.0.1:9090/dsvs/pkcs7/v1?WSDL"
    headers = {'Content-type': 'text/xml', 'Accept': 'application/json'}

    body = """<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
        <Body>
            <verifyPkcs7 xmlns="http://v1.pkcs7.plugin.server.dsv.eimzo.yt.uz/">
                <pkcs7B64 xmlns="">{}</pkcs7B64 >
            </verifyPkcs7 >
        </Body>
    </Envelope> """.format(pkcs7[0])

    response = requests.post(url, data=body, headers=headers)
    # my_file = open('response_first.txt', 'w')
    # my_file.write(response.content)
    # my_file.close()

    response.encoding = 'utf-8'
    my_json = response.text

    formatted_output = my_json.replace('\\n', '\n').replace('\\t', '\t')
    # my_file = open('output.txt', 'w')
    # my_file.write(formatted_output)
    # my_file.close()
    print(formatted_output)
    get_str = serializing(formatted_output)

    print(get_str)
    get_json = json.loads(get_str)
    index = 0

    print(get_json)
    print(report.signed)
    success = get_json["success"]
    signers = get_json["pkcs7Info"]["signers"][0]
    certificate = signers["certificate"][index]
    serialNumber = certificate["serialNumber"]
    subjectName = certificate["subjectName"]
    valid_from = certificate['validFrom']
    FULL_NAME = subjectName.split(',')[0].split('=')[1]
    print(FULL_NAME)  # ЗДЕСЬ ИМЯ КЛИЕНТА
    signAlgName = certificate['signature']['signAlgName']

    signature = certificate['signature']['signature']

    verified = signers['verified']
    certificateVerified = signers['certificateVerified']
    LINK = "http://e-otsenka.uz{}".format(report.pdf_report.url)  # Here is the link

    if sign_from == 1:
        report.pdf_qr_code_user = qr_code(signature, valid_from)
    else:
        report.pdf_qr_code_company = qr_code(signature, valid_from)
    report.signed = True
    report.save()


def verifyPkcs7(request):
    if request.method == "POST":
        pkcs7 = request.POST.get('pkcs7', None)
        report_id = request.POST.get('report_id', None)
        report = Report.objects.get(report_id=report_id)
        report.pdf_report_pkcs7 = []
        report.pdf_report_pkcs7.append(pkcs7)
        report.save()
        get_verifyPkcs7(report_id, int(request.POST.get('sign_from', 0)))
        data = {
            'success': 'True',
        }
        return JsonResponse(data)
    data = {
        'success': 'False',
    }
    return JsonResponse(data)


def get_car_from_search(request):
    car_number = request.GET.get('car_number', None)
    car = Car.objects.get(car_number=car_number)
    return car


def get_car_card(request):
    car = get_car_from_search(request)
    card = """<div class='card'><div class='card-header'> %s %s </div><div class='card-body'> <h5 class='card-title'>Введите ключ для скачивания</h5> <input type="text" id="key-input" class="form-control" required=""> </div> </div>""" % (
        car.brand, car.car_number,)
    data = {
        'card': card,
    }
    return JsonResponse(data)


def get_btn_to_download(request):
    key = request.GET.get('key', None)
    car = get_car_from_search(request)
    pdf_report = car.Car.select_related().get().pdf_report.url
    btn = "<a href='%s'><button class='btn enter_button'>Скачать</button></a>" % (pdf_report,)
    if key == get_key_from_car(car):
        data = {
            'btn': btn,
        }
        return JsonResponse(data)
    else:
        return JsonResponse(data=None)


def get_key_from_car(car):
    key = car.Car.select_related().get().key
    return key


def get_last_report_id(request):
    last_report = Report.objects.last()
    last_report_id = last_report.report_id
    return last_report_id


def get_service_ajax(request):
    service = get_service_from_request(request)
    print(service.price)
    print(service.name)
    print(get_brand_nph(request))
    data = {
        'name': service.name,
        'norm_per_hour': get_brand_nph(request),
        'price': service.price
    }
    return JsonResponse(data)


def get_product_ajax(request):
    product = get_product_from_request(request)

    data = {
        'name': product.name,
        'unit': product.unit,
        'price': product.price

    }
    return JsonResponse(data)


def get_consumable_ajax(request):
    consumable = get_consumable_from_request(request)

    data = {
        'name': consumable.name,
        'unit': consumable.unit,
        'price': consumable.price

    }
    return JsonResponse(data)


def get_wear_ajax(request):
    point = request.GET.get('point', None)
    weight = request.GET.get('weight', None)
    wear = ((0.208 - 0.003 * float(point)) * float(weight) ** 0.7) * 100

    data = {
        'wear': int(wear)
    }
    return JsonResponse(data)


def get_service_from_request(request):
    service_id = request.GET.get('service_id', None)
    finded_service = Service.objects.get(service_id=service_id)
    return finded_service


def get_product_from_request(request):
    product_id = request.GET.get('product_id', None)
    finded_product = Product.objects.get(product_id=product_id)
    return finded_product


def get_consumable_from_request(request):
    consumable_id = request.GET.get('consumable_id', None)
    finded_consumable = Consumable.objects.get(consumable_id=consumable_id)
    return finded_consumable


def get_brand_nph(request):
    service = get_service_from_request(request)
    brand = request.GET.get('brand', None)
    norm_per_hour = service.BRANDS.get(brand).value_from_object(service)
    return norm_per_hour


def get_service_cost(request):
    premium = request.GET.get('premium', None)
    norm_per_hour = request.GET.get('nph', None)
    price = request.GET.get('price', None).replace(" ", "")
    double_norm_per_hour = float(norm_per_hour)
    service_cost = int((double_norm_per_hour + float(premium) / 100 * double_norm_per_hour) * float(price))

    data = {
        'service_cost': service_cost,
    }
    return JsonResponse(data)


def get_product_cost(request):
    quantity = request.GET.get('quantity', None)
    price = request.GET.get('price', None).replace(" ", "")
    total_cost = int(float(quantity) * float(price))

    data = {
        'total_cost': total_cost,
    }
    return JsonResponse(data)


def get_consumable_cost(request):
    quantity = request.GET.get('quantity', None)
    price = request.GET.get('price', None).replace(" ", "")
    total_cost = int(float(quantity) * float(price))

    data = {
        'total_cost': total_cost,
    }
    return JsonResponse(data)


def calculate_service_cost(report, cost):
    print(cost)
    report.service_cost = report.service_cost + int(cost.replace(" ", ""))
    print("GOTTED")
    print(report.service_cost)

def calculate_product_cost(report, cost):
    print(cost)
    report.product_cost = report.product_cost + int(cost.replace(" ", ""))


def calculate_consumable_cost(report, cost):
    print(cost)
    report.consumable_cost = report.consumable_cost + int(cost.replace(" ", ""))
    print("GOTTED")
    print(report.consumable_cost)


def add_product_to_report(report, cost):
    if cost is None or cost == "":
        cost = 0
    calculate_product_cost(report, cost)


def add_service_to_report(report, service_id, cost):
    if cost is None or cost == "":
        cost = 0
    calculate_service_cost(report, cost)


def add_consumable_to_report(report, consumable_id, cost):
    if cost is None or cost == "":
        cost = 0
    calculate_consumable_cost(report, cost)


def get_data_from_service_form(form):
    if form.cleaned_data:
        service_data = {
            'service_id': form.cleaned_data['service_id'],
            'name': form.cleaned_data['name'],
            'norm_per_hour': form.cleaned_data['norm_per_hour'],
            'premium': form.cleaned_data['premium'],
            'price': form.cleaned_data['price'],
            'service_cost': form.cleaned_data['service_cost'],
        }
        return service_data


def get_data_from_product_form(form):
    product_data = {
        'name': form.cleaned_data['name'],
        # 'unit': form.cleaned_data['unit'],
        'quantity': form.cleaned_data['quantity'],
        'price': form.cleaned_data['price'],
        'product_cost': form.cleaned_data['product_cost'],
    }
    return product_data


def get_data_from_consum_form(form):
    consumable_data = {
        'consumable_id': form.cleaned_data['consumable_id'],
        'name': form.cleaned_data['name'],
        'unit': form.cleaned_data['unit'],
        'quantity': form.cleaned_data['quantity'],
        'price': form.cleaned_data['price'],
        'consumable_cost': form.cleaned_data['consumable_cost'],
    }
    return consumable_data


def get_data_from_wear_form(form):
    wear_data = {
        'point': checkOnNone(form.cleaned_data['point']),
        'weight': checkOnNone(form.cleaned_data['weight']),
        'wear': checkOnNone(form.cleaned_data['wear']),
        'accept_wear': checkOnNone(form.cleaned_data['accept_wear']),
    }
    print(wear_data)
    return wear_data


def checkOnNone(data):
    if data is None:
        return 0
    return data


# def get_report_cost(report, request):
#     accept_wear = request.GET.get('id_accept_wear', None)
#     wear = ((0.208 - 0.003 * float(point)) * float(weight) ** 0.7) * 100
#     total_report_cost
#
#     data = {
#         'total_report_cost': total_report_cost
#     }
#     return JsonResponse(data)
def response_image(link_img, link_delete, image, id):
    return {
        'errors': "",
        'initialPreview': [
            link_img
        ],
        'initialPreviewConfig': [{
            'caption': image.name,
            'width': '120px',
            'size': image.size,
            'url': link_delete,
            'key': id,
        }],
        'initialPreviewThumbTags': [

        ],
        'append': True
    }


def get_prices():
    prices = CustomSum.objects.order_by('sum')
    return prices


def create_report(request):
    car = Car.objects.create()
    car.save()
    customer = Customer.objects.create()
    customer.save()
    contract = Contract.objects.create(
        customer=customer
    )
    contract.save()
    report = Report.objects.create(
        car=car,
        contract=contract,
        created_by=request.user
    )
    report.save()
    calculation = Calculation.objects.create(
        report=report
    )
    calculation.save()
    return report


from django.core.paginator import Paginator


class CustomPaginator(Paginator):

    def _get_page(self, *args, **kwargs):
        self._page_custom = super()._get_page(*args, **kwargs)
        return self._page_custom

    @property
    def page_range(self):
        if self.num_pages < 10:
            return range(1, self.num_pages + 1)
        elif int(self.num_pages / 10) == int(self._page_custom.number / 10):
            previous = self._page_custom.number - self._page_custom.number % 10
            next = self.num_pages + 1
            return range(previous, next)
        else:
            remainder = self._page_custom.number % 10
            to_ten = 10 - remainder
            if self._page_custom.number / 10 < 1:
                remainder -= 1
            previous = self._page_custom.number - remainder
            next = self._page_custom.number + to_ten
            return range(previous, next)
