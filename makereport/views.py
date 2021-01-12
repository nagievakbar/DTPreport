from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.forms import formset_factory
from django.views.generic import View

from .forms import *
from .utils import *


class ReportView(View):
    decorators = [login_required]

    @method_decorator(decorators)
    def get(self, request, id=None):
        report = None
        if id:
            print('get method with report id=%.d' % id)
            report = Report.objects.get(report_id=id)
            contract = Contract.objects.get(contract_id=report.contract_id)
            report_form = ReportForm(instance=report)
            car = Car.objects.get(car_id=report.car_id)
            car.release_date = car.release_date.strftime('%Y')
            car_form = CarForm(instance=car)
            customer = Customer.objects.get(customer_id=contract.customer_id)
            customer_form = CustomerForm(instance=customer)
            service_form = formset_factory(ServiceForm, extra=1)
            service_formset = service_form(initial=report.SERVICE_DATA)
            product_form = formset_factory(ProductForm, extra=1)
            product_formset = product_form(initial=report.PRODUCT_DATA)
            consumable_form = formset_factory(ConsumableForm, extra=1)
            consumable_formset = consumable_form(initial=report.CONSUMABLE_DATA)
            wear_form = WearForm(initial=report.WEAR_DATA)
            total_price_report = report.get_total_report_price()
            print(total_price_report)
            template = 'makereport/edit_report.html'
            all_reports = Report.objects.all()
            if all_reports:
                report_number = Report.objects.filter(report_id=id).last()
            else:
                report_number = 1
        else:
            print('get method without id')
            report_form = ReportForm(instance=Report())
            car_form = CarForm(instance=Car())
            customer_form = CustomerForm(instance=Customer())
            service_form = formset_factory(ServiceForm, extra=2)
            service_formset = service_form(prefix='service')
            product_form = formset_factory(ProductForm, extra=2)
            product_formset = product_form(prefix='product')
            consumable_form = formset_factory(ConsumableForm, extra=2)
            consumable_formset = consumable_form(prefix='consumable')
            wear_form = WearForm()
            total_price_report = 0
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
            'service_formset': service_formset,
            'product_formset': product_formset,
            'consumable_formset': consumable_formset,
            'wear_form': wear_form,
            'report': report or None,
            'total_price_report': total_price_report
        }
        return render(request, template, context)

    @method_decorator(decorators)
    def post(self, request, id=None):
        total_report_price = 0
        if id:
            print('getting id')
            return self.put(request, id)
        report_form = ReportForm(request.POST, instance=Report())
        car_form = CarForm(request.POST, instance=Car())
        customer_form = CustomerForm(request.POST, instance=Customer())
        service_formset = self.init_service_formset(request)
        product_formset = self.init_product_formset(request)
        consumable_formset = self.init_consumable_formset(request)
        wear_form = WearForm(request.POST)
        all_reports = Report.objects.all()
        if all_reports:
            report_number = str(Report.objects.latest('created_at').report_id + 1)
        else:
            report_number = 1
        if report_form.is_valid() and car_form.is_valid() and customer_form.is_valid():
            new_contract = Contract()
            new_customer = customer_form.save(commit=False)
            new_customer.save()
            new_contract.customer = new_customer
            new_contract.save()
            new_report = report_form.save(commit=False)
            new_report.contract = new_contract
            new_car = car_form.save()
            new_car.save()
            new_report.car = new_car
            new_report.created_by = request.user
            new_report.save()
            print(new_report)
            for form in service_formset.forms:
                if form.is_valid():
                    print('service form is validated')
                    sd = get_data_from_service_form(form)
                    add_service_to_report(new_report, sd.__getitem__('service_id'), sd.__getitem__('service_cost'))
                    new_report.SERVICE_DATA.append(sd)
                print(new_report.service_cost)
            for form in product_formset.forms:
                if form.is_valid():
                    print('product form is validated')
                    pd = get_data_from_product_form(form)
                    add_product_to_report(new_report, pd.__getitem__('product_id'), pd.__getitem__('product_cost'))
                    new_report.PRODUCT_DATA.append(pd)
                print(new_report.product_cost)
            for form in consumable_formset.forms:
                if form.is_valid():
                    print('consum form is validated')
                    cd = get_data_from_consum_form(form)
                    add_consumable_to_report(new_report, cd.__getitem__('consumable_id'),
                                             cd.__getitem__('consumable_cost'))
                    new_report.CONSUMABLE_DATA.append(cd)
                print(new_report.consumable_cost)
            if wear_form.is_valid():
                print('wear form is validated')
                wd = get_data_from_wear_form(wear_form)
                new_report.WEAR_DATA.update(wd)
                new_report.get_total_report_price()
            new_report.save()
            return HttpResponseRedirect('/report/list')

        context = {
            'report_form': report_form,
            'car_form': car_form,
            'customer_form': customer_form,
            'report_number': report_number,
            'service_formset': service_formset,
            'product_formset': product_formset,
            'consumable_formset': consumable_formset,
            'wear_form': wear_form,
            # 'new_report': new_report or None,
            # 'total_report_price': total_report_price or None
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
        service_formset = self.init_service_formset(request)
        product_formset = self.init_product_formset(request)
        consumable_formset = self.init_consumable_formset(request)
        wear_form = WearForm(request.POST)
        # service_form = formset_factory(ServiceForm, extra=1)
        # service_formset = service_form(initial=report.SERVICE_DATA)
        # product_form = formset_factory(ProductForm, extra=1)
        # product_formset = product_form(initial=report.PRODUCT_DATA)
        # consumable_form = formset_factory(ConsumableForm, extra=1)
        # consumable_formset = consumable_form(initial=report.CONSUMABLE_DATA)
        # wear_form = WearForm(initial=report.WEAR_DATA)
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
            for form in service_formset.forms:
                if form.is_valid():
                    print('service form is validated')
                    sd = get_data_from_service_form(form)
                    add_service_to_report(new_report, sd.__getitem__('service_id'), sd.__getitem__('service_cost'))
                    new_report.SERVICE_DATA.append(sd)
                print(new_report.service_cost)
            for form in product_formset.forms:
                if form.is_valid():
                    print('product form is validated')
                    pd = get_data_from_product_form(form)
                    add_product_to_report(new_report, pd.__getitem__('product_id'), pd.__getitem__('product_cost'))
                    new_report.PRODUCT_DATA.append(pd)
                print(new_report.product_cost)
            for form in consumable_formset.forms:
                if form.is_valid():
                    print('consum form is validated')
                    cd = get_data_from_consum_form(form)
                    add_consumable_to_report(new_report, cd.__getitem__('consumable_id'),
                                             cd.__getitem__('consumable_cost'))
                    new_report.CONSUMABLE_DATA.append(cd)
                print(new_report.consumable_cost)
            if wear_form.is_valid():
                print('wear form is validated')
                wd = get_data_from_wear_form(wear_form)
                new_report.WEAR_DATA.update(wd)
                new_report.get_total_report_price()
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
        return render(request, 'makereport/delete_report.html', context=context)

    def init_service_formset(self, request):
        service_form = formset_factory(ServiceForm, extra=2)
        service_formset = service_form(request.POST, prefix='service')
        return service_formset

    def init_product_formset(self, request):
        product_form = formset_factory(ProductForm, extra=2)
        product_formset = product_form(request.POST, prefix='product')
        return product_formset

    def init_consumable_formset(self, request):
        consumable_form = formset_factory(ConsumableForm, extra=2)
        consumable_formset = consumable_form(request.POST, prefix='consumable')
        return consumable_formset


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
            return render(request, "makereport/auth/enter.html", context)
    else:
        return render(request, "makereport/auth/enter.html", context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))
