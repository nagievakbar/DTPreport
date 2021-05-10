from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
import os
from django.http import FileResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.core.files.storage import default_storage
from django.views.generic import View
from django.db.models import Q
from .forms import *
from .utils import *

from pdf_report.views import create_base64
from DTPreport import settings as s


class ImageDelete(View):
    def post(self, request):
        image = Images.objects.get(image_id=request.POST['key'])
        image.delete()
        return JsonResponse({'errors': True})


class ImageView(View):
    def post(self, request):
        hold_image = HoldsImages.objects.get(id=request.POST['id'])
        image = Images.objects.create(
            image=request.FILES['image'],
        )
        hold_image.image.add(image)
        hold_image.save()
        image.save()
        link_img = "{}{}".format(s.URL_FILES, image.image.url)
        print(link_img)
        link_delete = "{}/report/image/delete/".format(s.URL_FILES)
        return JsonResponse(
            response_image(link_img=link_img, link_delete=link_delete, image=image.image, id=image.image_id))


class PPhotoDelete(View):
    def post(self, request):
        image = PassportPhotos.objects.get(p_photo_id=request.POST['key'])
        image.delete()
        return JsonResponse({'errors': True})


class PPhotoView(View):
    def post(self, request):
        hold_image = HoldsImages.objects.get(id=request.POST['id'])
        image = PassportPhotos.objects.create(
            photo=request.FILES['photo'],
        )
        hold_image.pp_photo.add(image)
        hold_image.save()
        image.save()
        link_img = "{}{}".format(s.URL_FILES, image.photo.url)
        print(link_img)
        link_delete = "{}/report/pphoto/delete/".format(s.URL_FILES)
        return JsonResponse(
            response_image(link_img=link_img, link_delete=link_delete, image=image.photo, id=image.p_photo_id))


class OPhotoDelete(View):
    def post(self, request):
        image = OtherPhotos.objects.get(o_photo_id=request.POST['key'])
        image.delete()
        return JsonResponse({'errors': True})


class OPhotoView(View):
    def post(self, request, id=None):
        hold_image = HoldsImages.objects.get(id=request.POST['id'])
        image = OtherPhotos.objects.create(
            photos=request.FILES['photos'],
        )
        hold_image.o_images.add(image)
        hold_image.save()
        image.save()
        link_img = "{}{}".format(s.URL_FILES, image.photos.url)
        print(link_img)
        link_delete = "{}/report/ophoto/delete/".format(s.URL_FILES)
        return JsonResponse(
            response_image(link_img=link_img, link_delete=link_delete, image=image.photos, id=image.o_photo_id))


class ChecksDelete(View):
    def post(self, request):
        image = Checks.objects.get(checks_id=request.POST['key'])
        image.delete()
        return JsonResponse({'errors': True})


class ChecksView(View):
    def post(self, request, id=None):
        hold_image = HoldsImages.objects.get(id=request.POST['id'])
        image = Checks.objects.create(
            checks=request.FILES['checks'],
        )
        hold_image.checks.add(image)
        hold_image.save()
        image.save()
        link_img = "{}{}".format(s.URL_FILES, image.checks.url)
        print(link_img)
        link_delete = "{}/report/checks/delete/".format(s.URL_FILES)
        return JsonResponse(
            response_image(link_img=link_img, link_delete=link_delete, image=image.checks, id=image.checks_id))


def hold_image():
    last_hold = HoldsImages.objects.last()
    if last_hold is None or last_hold.report is not None:
        holds_image = HoldsImages.objects.create()
        print("CREATED NEW ONE ")
        holds_image.save()
        return holds_image
    for image in last_hold.image.all():
        image.delete()
    for pphotos in last_hold.pp_photo.all():
        pphotos.delete()
    for o_images in last_hold.o_images.all():
        o_images.delete()
    for checks in last_hold.checks.all():
        checks.delete()
    return last_hold


# Additional thingsss
class ReportEditView(View):
    decorators = [login_required]
    extend = False

    @method_decorator(decorators)
    def get(self, request, id=None):
        calculation = Calculation.objects.get(report_id=id)
        calculation_form = CalculationForm(instance=calculation)
        holds_image = HoldsImages.objects.get(report_id=id)
        new_hold_images = hold_image()
        new_hold_images.set_new(holds_image)
        images = new_hold_images.image_previous.all()
        pphotos = new_hold_images.pp_photo_previous.all()
        ophotos = new_hold_images.o_images_previous.all()
        checks = new_hold_images.checks_previous.all()
        image_form = ImageForm(instance=Images(), use_required_attribute=False)
        passphoto_form = PPhotoForm(instance=PassportPhotos(), use_required_attribute=False)
        otherphoto_form = OPhotoForm(instance=OtherPhotos(), use_required_attribute=False)
        checks_form = ChecksForm(instance=Checks(), use_required_attribute=False)
        report = Report.objects.get(report_id=id)
        contract = Contract.objects.get(contract_id=report.contract_id)
        contract_form = ContractForm(instance=contract)
        report_form = ReportForm(initial={'total_report_cost': report.total_report_cost}, instance=Report())
        car = Car.objects.get(car_id=report.car_id)
        car.release_date = car.release_date.strftime('%Y')
        car_form = CarForm(instance=car)
        customer = Customer.objects.get(customer_id=contract.customer_id)
        customer_form = CustomerForm(instance=customer)
        service_form = formset_factory(ServiceForm, extra=1)
        service_formset = service_form(initial=report.service_data, prefix='service')
        product_form = formset_factory(ProductForm, extra=1)
        product_formset = product_form(initial=report.product_data, prefix='product')
        consumable_form = formset_factory(ConsumableForm, extra=1)
        consumable_formset = consumable_form(initial=report.consumable_data, prefix='consumable')
        wear_form = WearForm(initial=report.wear_data)
        total_price_report = report.total_report_cost

        template = 'makereport/add_repor.html'
        context = {
            'id_image': new_hold_images.id,
            'calculation_form': calculation_form,
            'contract_form': contract_form,
            'report_form': report_form,
            'id': report.report_id,
            'prices': get_prices(),
            'car_form': car_form,
            'customer_form': customer_form,
            'service_formset': service_formset,
            'product_formset': product_formset,
            'consumable_formset': consumable_formset,
            'wear_form': wear_form,
            'report': report or None,
            'total_price_report': total_price_report,
            'image_form': image_form or None,
            'passphoto_form': passphoto_form or None,
            'otherphoto_form': otherphoto_form or None,
            'checks_form': checks_form or None,
            'images': images or None,
            'pphotos': pphotos or None,
            'ophotos': ophotos or None,
            'checks': checks or None,
        }
        return render(request, template, context)

    def post(self, request, id=None):
        holds_images = HoldsImages.objects.get(id=request.POST['id'])
        images = holds_images.image_concatinate()
        pphotos = holds_images.pp_photo_concatinate()
        ophotos = holds_images.o_photo_concatinate()
        checks = holds_images.check_concatinate()
        calculation_form = CalculationForm(request.POST, instance=Calculation())
        contract_form = ContractForm(request.POST, instance=Contract())
        report_form = ReportForm(request.POST, instance=Report())
        image_form = ImageForm(request.POST, request.FILES)
        passphoto_form = PPhotoForm(request.POST, request.FILES)
        otherphoto_form = OPhotoForm(request.POST, request.FILES)
        checks_form = ChecksForm(request.POST, request.FILES)
        car_form = CarForm(request.POST, instance=Car())
        customer_form = CustomerForm(request.POST, instance=Customer())
        service_formset = self.init_service_formset(request)
        product_formset = self.init_product_formset(request)
        consumable_formset = self.init_consumable_formset(request)
        wear_form = WearForm(request.POST)

        print("VALIDATION {}{}{}".format(report_form.is_valid(), car_form.is_valid(), customer_form.is_valid()))
        print(car_form.errors)
        if report_form.is_valid() \
                and car_form.is_valid() \
                and customer_form.is_valid() \
                and contract_form.is_valid() \
                and calculation_form.is_valid():
            new_contract = contract_form.save()
            new_customer = customer_form.save(commit=False)
            new_customer.save()
            new_contract.customer = new_customer
            new_contract.save()

            new_report = report_form.save(commit=False)
            new_report.contract = new_contract
            new_car = car_form.save()
            new_car.save()
            new_report.car = new_car
            new_report.created_by = request.user.myuser
            new_report.save()
            holds_images.report = new_report
            holds_images.store_add()
            holds_images.save()
            new_calculation = calculation_form.save()
            new_calculation.report = new_report
            new_calculation.save()
            new_report.service_data = []
            new_report.product_data = []
            new_report.consumable_data = []
            new_report.wear_data = {}
            for form in service_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    sd = get_data_from_service_form(form)
                    add_service_to_report(new_report, sd.__getitem__('service_id'), sd.__getitem__('service_cost'))
                    new_report.service_data.append(sd)
            for form in product_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    pd = get_data_from_product_form(form)
                    add_product_to_report(new_report, pd.__getitem__('product_id'), pd.__getitem__('product_cost'))
                    new_report.product_data.append(pd)
            for form in consumable_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    cd = get_data_from_consum_form(form)
                    add_consumable_to_report(new_report, cd.__getitem__('consumable_id'),
                                             cd.__getitem__('consumable_cost'))
                    new_report.consumable_data.append(cd)
            if wear_form.is_valid():
                wd = get_data_from_wear_form(wear_form)
                new_report.wear_data.update(wd)
                new_report.get_total_report_price()
            new_report.set_private_key()
            new_report.save()
            create_base64(request, new_report)
            return HttpResponseRedirect('/report/list_edit')

        context = {
            'id_image': holds_images.id,
            'calculation_form': calculation_form,
            'contract_form': contract_form,
            'report_form': report_form,
            'id': holds_images.report.report_id,
            'prices': get_prices(),
            'car_form': car_form,
            'customer_form': customer_form,
            'service_formset': service_formset,
            'product_formset': product_formset,
            'consumable_formset': consumable_formset,
            'wear_form': wear_form,
            'image_form': image_form,
            'passphoto_form': passphoto_form,
            'otherphoto_form': otherphoto_form,
            'checks_form': checks_form,
            'images': images or None,
            'pphotos': pphotos or None,
            'ophotos': ophotos or None,
            'checks': checks or None,
        }
        return render(request, 'makereport/add_repor.html', context)

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


class ReportView(View):
    decorators = [login_required]
    extend = False

    @method_decorator(decorators)
    def get(self, request, id=None, extend=0):
        report = None
        images = None
        pphotos = None
        ophotos = None
        checks = None
        if id:
            report_id = id
            holds_image = HoldsImages.objects.get(report_id=id)
            images = holds_image.image.all()
            pphotos = holds_image.pp_photo.all()
            ophotos = holds_image.o_images.all()
            checks = holds_image.checks.all()
            calculation = Calculation.objects.get(report_id=id)
            calculation_form = calculation
            image_form = ImageForm(instance=Images(), use_required_attribute=False)
            passphoto_form = PPhotoForm(instance=PassportPhotos(), use_required_attribute=False)
            otherphoto_form = OPhotoForm(instance=OtherPhotos(), use_required_attribute=False)
            checks_form = ChecksForm(instance=Checks(), use_required_attribute=False)
            report = Report.objects.get(report_id=id)
            contract = Contract.objects.get(contract_id=report.contract_id)
            contract_form = ContractForm(instance=contract)
            report_form = ReportForm(instance=report)
            car = Car.objects.get(car_id=report.car_id)
            car.release_date = car.release_date.strftime('%Y')
            car_form = CarForm(instance=car)
            customer = Customer.objects.get(customer_id=contract.customer_id)
            customer_form = CustomerForm(instance=customer)
            service_form = formset_factory(ServiceForm, extra=1)
            service_formset = service_form(initial=report.service_data, prefix='service')
            product_form = formset_factory(ProductForm, extra=1)
            product_formset = product_form(initial=report.product_data, prefix='product')
            consumable_form = formset_factory(ConsumableForm, extra=1)
            consumable_formset = consumable_form(initial=report.consumable_data, prefix='consumable')
            wear_form = WearForm(initial=report.wear_data)
            total_price_report = report.total_report_cost

            template = 'makereport/edit_repor.html'
        else:
            report_id = 0
            calculation_form = CalculationForm(instance=Calculation())
            image_form = ImageForm(instance=Images())
            contract_form = ContractForm(instance=Contract())
            passphoto_form = PPhotoForm(instance=PassportPhotos())
            otherphoto_form = OPhotoForm(instance=OtherPhotos())
            checks_form = ChecksForm(instance=Checks())
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
            template = 'makereport/add_repor.html'
            holds_image = hold_image()

        context = {
            'id_image': holds_image.id,
            'id': report_id,
            'calculation_form': calculation_form,
            'contract_form': contract_form,
            'report_form': report_form,
            'car_form': car_form,
            'prices': get_prices(),
            'customer_form': customer_form,
            'service_formset': service_formset,
            'product_formset': product_formset,
            'consumable_formset': consumable_formset,
            'wear_form': wear_form,
            'report': report or None,
            'total_price_report': total_price_report,
            'image_form': image_form or None,
            'passphoto_form': passphoto_form or None,
            'otherphoto_form': otherphoto_form or None,
            'checks_form': checks_form or None,
            'images': images or None,
            'pphotos': pphotos or None,
            'ophotos': ophotos or None,
            'checks': checks or None,
        }
        return render(request, template, context)

    @method_decorator(decorators)
    def post(self, request, id=None, extend=0):
        total_report_price = 0

        if id:
            return self.put(request, id)
        print("THIS IS HERE")
        holds_images = HoldsImages.objects.get(id=request.POST['id'])
        images = holds_images.image.all()
        pphotos = holds_images.pp_photo.all()
        ophotos = holds_images.o_images.all()
        checks = holds_images.checks.all()
        calculation_form = CalculationForm(request.POST, instance=Calculation())
        contract_form = ContractForm(request.POST, instance=Contract())
        report_form = ReportForm(request.POST, instance=Report())
        image_form = ImageForm(instance=Images(), use_required_attribute=False)
        passphoto_form = PPhotoForm(instance=PassportPhotos(), use_required_attribute=False)
        otherphoto_form = OPhotoForm(instance=OtherPhotos(), use_required_attribute=False)
        checks_form = ChecksForm(instance=Checks(), use_required_attribute=False)
        car_form = CarForm(request.POST, instance=Car())
        customer_form = CustomerForm(request.POST, instance=Customer())
        service_formset = self.init_service_formset(request)
        product_formset = self.init_product_formset(request)
        consumable_formset = self.init_consumable_formset(request)
        wear_form = WearForm(request.POST)

        print("VALIDATION {}{}{}".format(report_form.is_valid(), car_form.is_valid(), customer_form.is_valid()))
        if report_form.is_valid() and car_form.is_valid() and customer_form.is_valid() and contract_form.is_valid() and calculation_form.is_valid():

            new_contract = contract_form.save()
            new_customer = customer_form.save(commit=False)
            new_customer.save()
            new_contract.customer = new_customer
            new_contract.save()
            new_report = report_form.save(commit=False)
            new_report.contract = new_contract

            new_car = car_form.save()
            new_car.save()
            new_report.car = new_car
            new_report.created_by = request.user.myuser
            new_report.save()
            holds_images.report = new_report
            holds_images.save()
            new_calculation = calculation_form.save()
            new_calculation.report = new_report
            new_calculation.save()
            new_report.service_data = []
            new_report.product_data = []
            new_report.consumable_data = []
            new_report.wear_data = {}
            for form in service_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    sd = get_data_from_service_form(form)
                    add_service_to_report(new_report, sd.__getitem__('service_id'), sd.__getitem__('service_cost'))
                    new_report.service_data.append(sd)
            for form in product_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    pd = get_data_from_product_form(form)
                    add_product_to_report(new_report, pd.__getitem__('product_id'), pd.__getitem__('product_cost'))
                    new_report.product_data.append(pd)
            for form in consumable_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    cd = get_data_from_consum_form(form)
                    add_consumable_to_report(new_report, cd.__getitem__('consumable_id'),
                                             cd.__getitem__('consumable_cost'))
                    new_report.consumable_data.append(cd)
            if wear_form.is_valid():
                wd = get_data_from_wear_form(wear_form)
                new_report.wear_data.update(wd)
                new_report.get_total_report_price()
            new_report.set_private_key()
            new_report.save()
            create_base64(request, new_report)
            return HttpResponseRedirect('/report/list')

        context = {
            'id_image': holds_images.id,
            'calculation_form': calculation_form,
            'contract_form': contract_form,
            'report_form': report_form,
            'prices': get_prices(),
            'id': 0,
            'car_form': car_form,
            'customer_form': customer_form,
            'service_formset': service_formset,
            'product_formset': product_formset,
            'consumable_formset': consumable_formset,
            'wear_form': wear_form,
            'image_form': image_form,
            'passphoto_form': passphoto_form,
            'otherphoto_form': otherphoto_form,
            'checks_form': checks_form,
            'images': images or None,
            'pphotos': pphotos or None,
            'ophotos': ophotos or None,
            'checks': checks or None,
        }
        return render(request, 'makereport/add_repor.html', context)

    @method_decorator(decorators)
    def put(self, request, id=None):
        holds_images = HoldsImages.objects.get(id=request.POST['id'])
        images = holds_images.image.all()
        pphotos = holds_images.pp_photo.all()
        ophotos = holds_images.o_images.all()
        checks = holds_images.checks.all()
        calculation = Calculation.objects.get(report_id=id)
        report = Report.objects.get(report_id=id)
        contract = Contract.objects.get(contract_id=report.contract_id)
        contract_form = ContractFormEdit(instance=contract)
        image_form = ImageForm(instance=Images(), use_required_attribute=False)
        passphoto_form = PPhotoForm(instance=PassportPhotos(), use_required_attribute=False)
        otherphoto_form = OPhotoForm(instance=OtherPhotos(), use_required_attribute=False)
        checks_form = ChecksForm(instance=Checks(), use_required_attribute=False)

        car = Car.objects.get(car_id=report.car_id)
        car_form = CarForm(request.POST, instance=car)
        customer = Customer.objects.get(customer_id=contract.customer_id)
        customer_form = CustomerFormEdit(request.POST, instance=customer)
        service_formset = self.init_service_formset(request)
        product_formset = self.init_product_formset(request)
        consumable_formset = self.init_consumable_formset(request)
        wear_form = WearForm(request.POST)
        print("VALIDATION {}{}".format(car_form.is_valid(), customer_form.is_valid()))
        print(service_formset)

        # report_form.is_valid() and 
        if car_form.is_valid() and customer_form.is_valid():
            new_contract = contract
            new_customer = customer_form.save(commit=False)
            new_customer.save()
            new_contract.customer = new_customer
            new_contract.save()
            new_report = report
            new_report.contract = new_contract
            new_car = car_form.save()
            new_car.save()
            new_report.car = new_car
            new_report.created_by = request.user.myuser
            new_report.save()
            new_report.product_data.clear()
            new_report.service_data.clear()
            new_report.consumable_data.clear()
            report.consumable.clear()
            report.service.clear()
            report.product.clear()
            for form in service_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    sd = get_data_from_service_form(form)
                    add_service_to_report(new_report, sd.__getitem__('service_id'), sd.__getitem__('service_cost'))
                    new_report.service_data.append(sd)
            for form in product_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    pd = get_data_from_product_form(form)
                    add_product_to_report(new_report, pd.__getitem__('product_id'), pd.__getitem__('product_cost'))
                    new_report.product_data.append(pd)
            for form in consumable_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    cd = get_data_from_consum_form(form)
                    add_consumable_to_report(new_report, cd.__getitem__('consumable_id'),
                                             cd.__getitem__('consumable_cost'))
                    new_report.consumable_data.append(cd)
            if wear_form.is_valid():
                wd = get_data_from_wear_form(wear_form)
                new_report.wear_data.update(wd)
                new_report.get_total_report_price()
            new_report.save()
            create_base64(request, new_report)
            return HttpResponseRedirect('/report/list')

        context = {
            'id_image': holds_images.id,
            'contract_form': contract_form,
            'prices': get_prices(),
            'car_form': car_form,
            'id': id,
            'customer_form': customer_form,
            'image_form': image_form,
            'passphoto_form': passphoto_form,
            'otherphoto_form': otherphoto_form,
            'checks_form': checks_form,
            'service_formset': service_formset,
            'product_formset': product_formset,
            'consumable_formset': consumable_formset,
            'wear_form': wear_form,
            'images': images or None,
            'pphotos': pphotos or None,
            'ophotos': ophotos or None,
            'checks': checks or None,
        }
        return render(request, 'makereport/edit_repor.html', context)

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
    if request.user.is_superuser:
        return admin_list(request)
    else:
        return user_list_some(request)


@login_required
def reports_edit_list(request):
    if 'search' in request.GET:
        reports = Report.objects.filter(car__car_number=request.GET['search'])
    else:
        reports = Report.objects.all()
    return render(request, 'makereport/additional.html', context={'reports': reports})


def user_list_some(request):
    if 'search' in request.GET:
        reports = Report.objects.filter(car__car_number__contains=request.GET['search'], created_by=request.user.myuser)
    else:
        reports = Report.objects.filter(created_by=request.user)
    return render(request, 'makereport/index.html', context={'reports': reports})


def admin_list(request):
    if 'search' in request.GET:
        reports = Report.objects.filter(
            car__car_number__contains=request.GET['search'])
    else:
        reports = Report.objects.all()

    return render(request, 'makereport/index.html', context={'reports': reports})


@login_required
def users_list(request):
    users = User.objects.all()
    return render(request, 'makereport/users_list.html', context={'users': users})


@login_required
def get_template(request):
    try:
        TemplateBase.objects.first().delete()
    finally:
        new_template = TemplateBase.objects.create()
        new_template.template = request.FILES['file']
        new_template.save()
        return JsonResponse({})


@login_required
def get_template_mixing(request):
    try:
        TemplateMixing.objects.first().delete()
    finally:
        new_template = TemplateMixing.objects.create()
        new_template.template = request.FILES['file']
        new_template.save()
        return JsonResponse({})


@login_required
def get_template_agreement(request):
    try:
        TemplateAgreement.objects.first().delete()
    finally:
        new_template = TemplateAgreement.objects.create()
        new_template.template = request.FILES['file']
        new_template.save()
        return JsonResponse({})




def delete_old(template):
    if template is not None:
        template.delete()


class UserSettingsView(View):
    decorators = [login_required]

    @method_decorator(decorators)
    def get(self, request):
        user = request.user.myuser
        templateForm = TemplateForm()
        context = {
            'user': user,
            'form_upload': templateForm
        }
        return render(request, 'makereport/user_settings.html', context)


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
            context["error"] = True
            context["description"] = "Введен неправильный логин или пароль"
            return render(request, "makereport/auth/login_sea.html", context)
    else:
        if request.user.is_anonymous:
            return render(request, "makereport/auth/login_sea.html", context)
        else:
            return redirect('reports_list')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))


def search(request):
    errors = "Введите ключ"
    if 'key' in request.GET:
        report = Report.objects.filter(key=request.GET['key'])
        if report.exists():
            return HttpResponseRedirect('pdf/{}/'.format(report.first().report_id))
        else:
            errors = 'Такого ключа не существует'
    context = {
        'errors': errors
    }
    return render(request, "makereport/auth/search.html", context=context)
