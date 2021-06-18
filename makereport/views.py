from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from django.utils.decorators import method_decorator

from django.views.generic import View
from django.db.models import Q
from .forms import *
from .utils import *

from pdf_report.views import create_base64
from DTPreport import settings as s
from pdf_report.tasks import reduce_image, delete_empty_report, make_pdf, make_pdf_additional


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
        reduce_image.delay(image.image.path)
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
        reduce_image.delay(image.photo.path)
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
        reduce_image.delay(image.photos.path)
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
        reduce_image.delay(image.checks.path)
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
        new_hold_images = HoldsImages.objects.create()
        new_hold_images.set_new(holds_image)
        new_report = create_report(request)
        new_hold_images.report = new_report
        new_hold_images.save()
        images = new_hold_images.image_previous.all()
        pphotos = new_hold_images.pp_photo_previous.all()
        ophotos = new_hold_images.o_images_previous.all()
        checks = new_hold_images.checks_previous.all()
        image_form = ImageForm(instance=Images(), use_required_attribute=False)
        passphoto_form = PPhotoForm(instance=PassportPhotos(), use_required_attribute=False)
        otherphoto_form = OPhotoForm(instance=OtherPhotos(), use_required_attribute=False)
        checks_form = ChecksForm(instance=Checks(), use_required_attribute=False)
        report = Report.objects.get(report_id=id)
        report.consumable_cost = 0
        report.product_cost = 0
        report.service_cost = 0
        contract = Contract.objects.get(contract_id=report.contract_id)
        contract_form = ContractForm(instance=contract)
        report_form = ReportForm(instance=Report())
        car = Car.objects.get(car_id=report.car_id)
        car.release_date = car.release_date
        car_form = CarForm(instance=car)
        customer = Customer.objects.get(customer_id=contract.customer_id)
        customer_form = CustomerForm(instance=customer)
        service_form = formset_factory(ServiceForm, extra=1)
        service_formset = service_form(prefix='service')
        product_form = formset_factory(ProductForm, extra=1)
        product_formset = product_form(prefix='product')
        consumable_form = formset_factory(ConsumableForm, extra=1)
        consumable_formset = consumable_form(prefix='consumable')
        wear_form = WearForm(initial=report.wear_data)
        total_price_report = report.total_report_cost

        template = 'makereport/add_repor.html'
        context = {
            'base': False,
            'id_image': new_hold_images.id,
            'calculation_form': calculation_form,
            'contract_form': contract_form,
            'report_form': report_form,
            'id': new_report.report_id,
            'prices': get_prices(),
            'car_form': car_form,
            'customer_form': customer_form,
            'service_formset': service_formset,
            'product_formset': product_formset,
            'consumable_formset': consumable_formset,
            'wear_form': wear_form,
            'report': new_report or None,
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
        holds_images = HoldsImages.objects.get(id=request.POST['id_image'])
        images = holds_images.image_concatinate()
        pphotos = holds_images.pp_photo_concatinate()
        ophotos = holds_images.o_photo_concatinate()
        checks = holds_images.check_concatinate()
        report_id = int(request.POST['id_report'])
        if report_id == 0:
            calculation_form = CalculationForm(request.POST, instance=Calculation())
            contract_form = ContractForm(request.POST, instance=Contract())
            report_form = ReportForm(request.POST, instance=Report())
            car_form = CarForm(request.POST, instance=Car())
            customer_form = CustomerForm(request.POST, instance=Customer())
        else:
            report = Report.objects.get(report_id=report_id)
            calculation = Calculation.objects.get(report_id=report_id)
            calculation_form = CalculationForm(request.POST, instance=calculation)
            contract_form = ContractForm(request.POST, instance=report.contract)
            report_form = ReportForm(request.POST, instance=report)
            car_form = CarForm(request.POST, instance=report.car)
            customer_form = CustomerForm(request.POST, instance=report.contract.customer)

        image_form = ImageForm(request.POST, request.FILES)
        passphoto_form = PPhotoForm(request.POST, request.FILES)
        otherphoto_form = OPhotoForm(request.POST, request.FILES)
        checks_form = ChecksForm(request.POST, request.FILES)

        service_formset = self.init_service_formset(request)
        product_formset = self.init_product_formset(request)
        consumable_formset = self.init_consumable_formset(request)
        wear_form = WearForm(request.POST)

        print("VALIDATION {}{}{}".format(report_form.is_valid(), car_form.is_valid(), customer_form.is_valid()))
        print(car_form.errors)
        context = {
            'base': False,
            'id_image': holds_images.id,
            'calculation_form': calculation_form,
            'contract_form': contract_form,
            'report_form': report_form,
            'id': report_id,
            'prices': get_prices(),
            'car_form': car_form,
            'customer_form': customer_form,
            'service_formset': service_formset,
            'product_formset': product_formset,
            'consumable_formset': consumable_formset,
            'report': None,
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
            new_report.created_by = request.user
            new_report.save()
            holds_images.report = new_report
            holds_images.store_add()
            new_calculation = calculation_form.save()
            new_calculation.report = new_report
            new_calculation.save()
            new_report.clean_incoming_data()
            for form in service_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    sd = get_data_from_service_form(form)
                    if sd.__getitem__('service_cost') is not None:
                        add_service_to_report(new_report, sd.__getitem__('service_id'), sd.__getitem__('service_cost'))
                        new_report.service_data.append(sd)
            for form in product_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    pd = get_data_from_product_form(form)
                    if pd.__getitem__('product_cost') is not None:
                        add_product_to_report(new_report, pd.__getitem__('product_cost'))
                        new_report.product_data.append(pd)
            for form in consumable_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    cd = get_data_from_consum_form(form)
                    if cd.__getitem__('consumable_cost') is not None:
                        add_consumable_to_report(new_report, cd.__getitem__('consumable_id'),
                                                 cd.__getitem__('consumable_cost'))
                        new_report.consumable_data.append(cd)
            if wear_form.is_valid():
                wd = get_data_from_wear_form(wear_form)
                new_report.wear_data.update(wd)
                new_report.get_total_report_price()
            new_report.set_private_key()
            new_report.save()
            total_price_report = new_report.total_report_cost
            context['id'] = new_report.report_id
            context['total_price_report'] = total_price_report
            context['report'] = new_report
            try:
                create_base64(new_report)
            except KeyError:
                pass
            make_pdf_additional.delay(new_report.report_id)

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
            calculation_form = CalculationForm(instance=calculation)
            image_form = ImageForm(instance=Images(), use_required_attribute=False)
            passphoto_form = PPhotoForm(instance=PassportPhotos(), use_required_attribute=False)
            otherphoto_form = OPhotoForm(instance=OtherPhotos(), use_required_attribute=False)
            checks_form = ChecksForm(instance=Checks(), use_required_attribute=False)
            report = Report.objects.get(report_id=id)
            contract = Contract.objects.get(contract_id=report.contract_id)
            contract_form = ContractForm(instance=contract)
            report_form = ReportForm(instance=report)
            car = Car.objects.get(car_id=report.car_id)
            car.release_date = car.release_date
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
            # template = 'makereport/edit_repor.html'
        else:
            report = create_report(request)
            report_id = report.report_id
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
            holds_image = HoldsImages.objects.create()
            holds_image.report = report
            holds_image.save()
        template = 'makereport/add_repor.html'
        context = {
            'base': True,
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
        print("ID REPORT")

        if int(request.POST['id_report']) != 0:
            id = int(request.POST['id_report'])
        if id:
            return self.put(request, id)
        print("THIS IS HERE")
        holds_images = HoldsImages.objects.get(id=request.POST['id_image'])
        images = holds_images.image.all()
        pphotos = holds_images.pp_photo.all()
        ophotos = holds_images.o_images.all()
        checks = holds_images.checks.all()
        calculation_form = CalculationForm(request.POST, instance=Calculation())
        contract_form = ContractForm(request.POST, instance=Contract())
        report_form = ReportForm(request.POST, instance=Report())
        car_form = CarForm(request.POST, instance=Car())
        customer_form = CustomerForm(request.POST, instance=Customer())
        image_form = ImageForm(instance=Images(), use_required_attribute=False)
        passphoto_form = PPhotoForm(instance=PassportPhotos(), use_required_attribute=False)
        otherphoto_form = OPhotoForm(instance=OtherPhotos(), use_required_attribute=False)
        checks_form = ChecksForm(instance=Checks(), use_required_attribute=False)
        service_formset = self.init_service_formset(request)
        product_formset = self.init_product_formset(request)
        consumable_formset = self.init_consumable_formset(request)
        wear_form = WearForm(request.POST)
        context = {
            'base': True,
            'id_image': holds_images.id,
            'id': 0,
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
            'report': None,
            'image_form': image_form or None,
            'passphoto_form': passphoto_form or None,
            'otherphoto_form': otherphoto_form or None,
            'checks_form': checks_form or None,
            'images': images or None,
            'pphotos': pphotos or None,
            'ophotos': ophotos or None,
            'checks': checks or None,
        }
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
            new_report.created_by = request.user
            new_report.save()
            holds_images.report = new_report
            holds_images.save()
            new_calculation = calculation_form.save()
            new_calculation.report = new_report
            new_calculation.save()
            new_report.clean_incoming_data()
            for form in service_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    sd = get_data_from_service_form(form)
                    print(sd)
                    add_service_to_report(new_report, sd.__getitem__('service_id'), sd.__getitem__('service_cost'))
                    new_report.service_data.append(sd)
            for form in product_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    pd = get_data_from_product_form(form)
                    add_product_to_report(new_report, pd.__getitem__('product_cost'))
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
            total_price_report = new_report.total_report_cost
            context['id'] = new_report.report_id
            context['total_price_report'] = total_price_report
            context['report'] = new_report
            try:
                create_base64(new_report)
            except KeyError:
                pass
            make_pdf.delay(new_report.report_id)
        return render(request, 'makereport/add_repor.html', context)

    @method_decorator(decorators)
    def put(self, request, id=None):
        holds_images = HoldsImages.objects.get(id=request.POST['id_image'])
        images = holds_images.image.all()
        pphotos = holds_images.pp_photo.all()
        ophotos = holds_images.o_images.all()
        checks = holds_images.checks.all()
        calculation = Calculation.objects.get(report_id=id)
        report = Report.objects.get(report_id=id)
        car = Car.objects.get(car_id=report.car_id)
        contract = Contract.objects.get(contract_id=report.contract_id)
        customer = Customer.objects.get(customer_id=contract.customer_id)
        contract_form = ContractFormEdit(request.POST, instance=contract)
        car_form = CarForm(request.POST, instance=car)
        calculation_form = CalculationForm(request.POST, instance=calculation)
        report_form = ReportForm(request.POST, instance=report)
        customer_form = CustomerForm(request.POST, instance=customer)
        image_form = ImageForm(instance=Images(), use_required_attribute=False)
        passphoto_form = PPhotoForm(instance=PassportPhotos(), use_required_attribute=False)
        otherphoto_form = OPhotoForm(instance=OtherPhotos(), use_required_attribute=False)
        checks_form = ChecksForm(instance=Checks(), use_required_attribute=False)
        service_formset = self.init_service_formset(request)
        product_formset = self.init_product_formset(request)
        consumable_formset = self.init_consumable_formset(request)
        wear_form = WearForm(request.POST)
        print(
            "VALIDATION {}{} {} {} {}".format(report_form.is_valid(), car_form.is_valid(), customer_form.is_valid(),
                                              contract_form.is_valid(), calculation_form.is_valid()))

        context = {
            'base': True,
            'id_image': holds_images.id,
            'id': id,
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
            'image_form': image_form or None,
            'passphoto_form': passphoto_form or None,
            'otherphoto_form': otherphoto_form or None,
            'checks_form': checks_form or None,
            'images': images or None,
            'pphotos': pphotos or None,
            'ophotos': ophotos or None,
            'checks': checks or None,
        }

        # report_form.is_valid() and
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
            new_report.created_by = request.user
            new_report.save()
            holds_images.report = new_report
            holds_images.save()
            new_calculation = calculation_form.save()
            new_calculation.report = new_report
            new_calculation.save()
            new_report.clean_incoming_data()
            for form in service_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    sd = get_data_from_service_form(form)
                    add_service_to_report(new_report, sd.__getitem__('service_id'), sd.__getitem__('service_cost'))
                    new_report.service_data.append(sd)
            for form in product_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    pd = get_data_from_product_form(form)
                    print(pd.__getitem__('product_cost'))
                    add_product_to_report(new_report, pd.__getitem__('product_cost'))
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

            if new_report.key is None or new_report.key == "":
                new_report.set_private_key()
            new_report.save()

            context['report'] = new_report
            total_price_report = new_report.total_report_cost
            context['total_price_report'] = total_price_report
            try:
                create_base64(new_report)
            except KeyError:
                pass

            finally:
                make_pdf.delay(new_report.report_id)
                context = {
                    'base': True,
                    'id_image': holds_images.id,
                    'id': id,
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
                    'report': new_report,
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
                print("PRODUCT_COST")
                print(new_report.product_cost)
                return render(request, 'makereport/add_repor.html', context)
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


def delete(request):
    try:
        report = Report.objects.get(report_id=request.GET.get('id', 0))
        report.delete()
    finally:
        pass
    return JsonResponse({})


@login_required
def reports_list(request):
    return admin_list(request)


@login_required
def reports_edit_list(request):
    if 'search' in request.GET:
        reports = Report.objects.filter(car__car_number__contains=request.GET['search']).exclude(
            (Q(key__isnull=True) | Q(key__exact='')))
    else:
        reports = Report.objects.exclude((Q(key__isnull=True) | Q(key__exact=''))).order_by('-report_id')
    paginator = CustomPaginator(reports, 10)
    page_number = request.GET.get('page')
    reports = paginator.get_page(page_number)
    return render(request, 'makereport/additional.html', context={'reports': reports})


def user_list_some(request):
    if 'search' in request.GET:
        reports = Report.objects.filter(car__car_number__contains=request.GET['search'], created_by=request.user)
    else:
        reports = Report.objects.filter(created_by=request.user)
    return render(request, 'makereport/index.html', context={'reports': reports})


def admin_list(request):
    if 'search' in request.GET:
        reports = Report.objects.filter(
            Q(car__car_number__contains=request.GET['search'])).exclude((Q(key__isnull=True) | Q(key__exact='')))
    else:
        reports = Report.objects.all().exclude((Q(key__isnull=True) | Q(key__exact=''))).order_by('-report_id')
    paginator = CustomPaginator(reports, 10)
    page_number = request.GET.get('page')
    reports = paginator.get_page(page_number)
    return render(request, 'makereport/index.html', context={'reports': reports})


@login_required
def users_list(request):
    users = User.objects.all()
    return render(request, 'makereport/users_list.html', context={'users': users})


@login_required
def get_template(request):
    print("COMMING")
    try:
        TemplateBase.objects.last().delete()
    finally:
        new_template = TemplateBase.objects.create()
        new_template.template = request.FILES['file']
        new_template.save()
        return JsonResponse({})


@login_required
def get_template_mixing(request):
    try:
        TemplateMixing.objects.last().delete()
    finally:
        new_template = TemplateMixing.objects.create()
        new_template.template = request.FILES['file']
        new_template.save()
        return JsonResponse({})


@login_required
def get_template_agreement(request):
    try:
        TemplateAgreement.objects.last().delete()
    finally:
        new_template = TemplateAgreement.objects.create()
        new_template.template = request.FILES['file']
        new_template.save()
        return JsonResponse({})


@login_required
def get_template_additional(request):
    try:
        TemplateAdditional.objects.last().delete()
    finally:
        new_template = TemplateAdditional.objects.create()
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
        return render(request, 'makereport/user_settings.html')


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


def reduce_documents_size(request):
    document = Documents.objects.first()
    reduce_image.delay(document.license.path)
    reduce_image.delay(document.guvonhnoma.path)
    reduce_image.delay(document.certificate.path)
    reduce_image.delay(document.insurance.path)
    return JsonResponse({})


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
