from .models import *
from django.http import JsonResponse


def get_car_from_search(request):
    car_number = request.GET.get('car_number', None)
    car = Car.objects.get(car_number=car_number)

    data = {

    }
    return JsonResponse(data)


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
    price = request.GET.get('price', None)
    service_cost = int((float(norm_per_hour) + float(premium)) * float(price))

    data = {
        'service_cost': service_cost,
    }
    return JsonResponse(data)


def get_product_cost(request):
    quantity = request.GET.get('quantity', None)
    price = request.GET.get('price', None)
    total_cost = int(float(quantity) * float(price))

    data = {
        'total_cost': total_cost,
    }
    return JsonResponse(data)


def get_consumable_cost(request):
    quantity = request.GET.get('quantity', None)
    price = request.GET.get('price', None)
    total_cost = int(float(quantity) * float(price))

    data = {
        'total_cost': total_cost,
    }
    return JsonResponse(data)


def add_service_to_report(report, service_id, cost):
    report.service.add(Service.objects.get(service_id=service_id))
    calculate_service_cost(report, cost)


def calculate_service_cost(report, cost):
    report.service_cost = report.service_cost + cost


def add_product_to_report(report, product_id, cost):
    report.product.add(Product.objects.get(product_id=product_id))
    calculate_product_cost(report, cost)


def calculate_product_cost(report, cost):
    report.product_cost = report.product_cost + cost


def add_consumable_to_report(report, consumable_id, cost):
    report.consumable.add(Consumable.objects.get(consumable_id=consumable_id))
    calculate_consumable_cost(report, cost)


def calculate_consumable_cost(report, cost):
    report.consumable_cost = report.consumable_cost + cost


def get_data_from_service_form(form):
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
        'product_id': form.cleaned_data['product_id'],
        'name': form.cleaned_data['name'],
        'unit': form.cleaned_data['unit'],
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
        'point': form.cleaned_data['point'],
        'weight': form.cleaned_data['weight'],
        'wear': form.cleaned_data['wear'],
        'accept_wear': form.cleaned_data['accept_wear'],
    }
    return wear_data


# def get_report_cost(report, request):
#     accept_wear = request.GET.get('id_accept_wear', None)
#     wear = ((0.208 - 0.003 * float(point)) * float(weight) ** 0.7) * 100
#     total_report_cost
#
#     data = {
#         'total_report_cost': total_report_cost
#     }
#     return JsonResponse(data)