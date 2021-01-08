from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator

from django.contrib.auth import authenticate, login, logout
from django.forms import formset_factory
from .forms import *
from django.views.generic import View


class ReportView(View):
    decorators = [login_required]

    @method_decorator(decorators)
    def get(self, request, id=None):
        if id:
            report = Report.objects.get(report_id=id)
            contract = Contract.objects.get(contract_id=report.contract_id)
            report_form = ReportForm(instance=report)
            car = Car.objects.get(car_id=report.car_id)
            car.release_date = car.release_date.strftime('%Y')
            car_form = CarForm(instance=car)
            customer = Customer.objects.get(customer_id=contract.customer_id)
            customer_form = CustomerForm(instance=customer)
            service_form = formset_factory(ServiceForm, extra=2)
            service_formset = service_form()
            product_form = formset_factory(ProductForm, extra=2)
            product_formset = product_form()
            consumable_form = formset_factory(ConsumableForm, extra=2)
            consumable_formset = consumable_form()
            template = 'makereport/edit_report.html'
            all_reports = Report.objects.all()
            if all_reports:
                report_number = Report.objects.filter(report_id=id).last()
            else:
                report_number = 1
        else:
            report_form = ReportForm(instance=Report())
            car_form = CarForm(instance=Car())
            customer_form = CustomerForm(instance=Customer())
            service_form = formset_factory(ServiceForm, extra=2)
            service_formset = service_form()
            product_form = formset_factory(ProductForm, extra=2)
            product_formset = product_form()
            consumable_form = formset_factory(ConsumableForm, extra=2)
            consumable_formset = consumable_form()
            template = 'makereport/add_report.html'
            all_reports = Report.objects.all()
            if all_reports:
                report_number = str(Report.objects.latest('created_at').report_id + 1)
            else:
                report_number = 1

        context = {
            'report_form': report_form,
            'car_form': car_form,
            'customer_form': customer_form,
            'report_number': report_number,
            'service_formset' : service_formset,
            'product_formset': product_formset,
            'consumable_formset':consumable_formset,
        }
        return render(request, template, context)

    @method_decorator(decorators)
    def post(self, request, id=None):
        if id:
            print('getting id')
            return self.put(request, id)
        report_form = ReportForm(request.POST, instance=Report())
        car_form = CarForm(request.POST, instance=Car())
        customer_form = CustomerForm(request.POST, instance=Customer())
        service_form = formset_factory(ServiceForm, extra=2)
        service_formset = service_form()
        print(service_form)
        print('\nservice_form')
        print(service_formset)
        print('\nservice_formset')
        all_reports = Report.objects.all()
        if all_reports:
            report_number = str(Report.objects.latest('created_at').report_id + 1)
        else:
            report_number = 1
        if report_form.is_valid() and car_form.is_valid() and customer_form.is_valid():
            new_contract = Contract()
            new_customer = customer_form.save(commit=False)
            new_customer.save()
            print(new_customer)
            print('\nnew_customer')
            new_contract.customer = new_customer
            new_contract.save()
            print(new_contract)
            print('\nnew_contract')
            new_report = report_form.save(commit=False)
            new_report.contract = new_contract
            new_car = car_form.save()
            new_car.save()
            new_report.car = new_car
            new_report.created_by = request.user
            print(service_formset)
            print('\nservice_formset')
            for form in service_formset:
                print(form)
                print('\nform')
                new_service = form.save()
                print(new_service)
                print('\nnew_service')
                new_report.service.add(new_service)
                print(new_report.service.get(new_service))
                print('\nnew_report.service.get(new_service)')
            new_report.save()
            return HttpResponseRedirect('/makereport/list')
        context = {
            'report_form': report_form,
            'car_form': car_form,
            'customer_form': customer_form,
            'report_number': report_number,
            'service_formset': service_formset,
        }
        return render(request, 'makereport/add_report.html', context)

    @method_decorator(decorators)
    def put(self, request, id=None):
        report = Report.objects.get(report_id=id)
        contract = Contract.objects.get(contract_id=report.contract_id)
        report_form = ReportForm(request.POST, instance=report)
        # report_form.created_at = report_form.created_at.strptime('%d. %m. %Y')
        car = Car.objects.get(car_id=report.car_id)
        car_form = CarForm(request.POST, instance=car)
        customer = Customer.objects.get(customer_id=contract.customer_id)
        customer_form = CustomerForm(request.POST, instance=customer)
        all_reports = Report.objects.all()
        if all_reports:
            report_number = Report.objects.get(report_id=id)
        else:
            report_number = 1
        if report_form.is_valid() and car_form.is_valid() and customer_form.is_valid():
            new_customer = customer_form.save(commit=False)
            new_customer.save()
            contract.customer = new_customer
            contract.save()
            new_report = report_form.save(commit=False)
            new_report.contract = contract
            new_car = car_form.save()
            new_car.save()
            new_report.car = new_car
            new_report.save()
            return HttpResponseRedirect('/report/list')
        context = {
            'report_form': report_form,
            'car_form': car_form,
            'customer_form': customer_form,
            'report_number': report_number,
        }
        return render(request, 'makereport/edit_report.html', context)

    @method_decorator(decorators)
    def delete(self, request, id=None):
        report = Report.objects.get(report_id=id)
        if request.method == 'POST':
            report.delete()
            return redirect('reports_list')
        context = {'report': report}
        return render(request, 'makereport/delete_report.html', context=report)


@login_required
def reports_list(request):
    reports = Report.objects.all()
    return render(request, 'makereport/index.html', context={'reports': reports})


@login_required
def users_list(request):
    users = User.objects.all()
    return render(request, 'makereport/users_list.html', context={'users': users})


def user_login(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('reports_list'))
        else:
            context["error"] = "Invalid data"
            return render(request, "makereport/auth/login.html", context)
    else:
        return render(request, "makereport/auth/login.html", context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))


def get_service_ajax(request):
    service = get_service_from_request(request)

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
    print(point)
    print(weight)
    wear =((0.208 - 0.003 * float(point)) * float(weight) ** 0.7) * 100

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

    total_cost = (float(norm_per_hour) + float(premium) ) * float(price)

    data = {
        'total_cost': round(total_cost),
    }
    return JsonResponse(data)

def get_product_cost(request):
    quantity = request.GET.get('quantity', None)
    price = request.GET.get('price', None)

    total_cost = float(quantity) * float(price)

    data = {
        'total_cost': total_cost,
    }
    return JsonResponse(data)


def get_consumable_cost(request):
    quantity = request.GET.get('quantity', None)
    price = request.GET.get('price', None)

    total_cost = float(quantity) * float(price)

    data = {
        'total_cost': total_cost,
    }
    return JsonResponse(data)