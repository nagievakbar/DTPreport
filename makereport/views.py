from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View

from .forms import *
from .utils import *
from .converters import num2text

from DTPreport import settings as s
from DTPreport import urls


class ReportView(View):
    decorators = [login_required]
    extend = False

    @method_decorator(decorators)
    def get(self, request, id=None, extend=0):
        report = None
        images = None
        pphotos = None
        ophotos = None
        if id:
            print('get method with report id=%.d' % id)
            images = Images.objects.filter(report_id=id)
            pphotos = PassportPhotos.objects.filter(report_id=id)
            ophotos = OtherPhotos.objects.filter(report_id=id)
            image_form = ImageForm(instance=Images())
            passphoto_form = PPhotoForm(instance=PassportPhotos())
            otherphoto_form = OPhotoForm(instance=OtherPhotos())
            report = Report.objects.get(report_id=id)
            contract = Contract.objects.get(contract_id=report.contract_id)
            report_form = ReportForm(instance=report)
            car = Car.objects.get(car_id=report.car_id)
            car.release_date = car.release_date.strftime('%Y')
            car_form = CarForm(instance=car)
            customer = Customer.objects.get(customer_id=contract.customer_id)
            customer_form = CustomerForm(instance=customer)
            if extend:
                service_form = formset_factory(ServiceForm, extra=2)
                service_formset = service_form(prefix='service')
                product_form = formset_factory(ProductForm, extra=2)
                product_formset = product_form(prefix='product')
                consumable_form = formset_factory(ConsumableForm, extra=2)
                consumable_formset = consumable_form(prefix='consumable')
                wear_form = WearForm()
                total_price_report = 0
            else:
                service_form = formset_factory(ServiceForm, extra=1)
                service_formset = service_form(initial=report.service_data, prefix='service')
                product_form = formset_factory(ProductForm, extra=1)
                product_formset = product_form(initial=report.product_data, prefix='product')
                consumable_form = formset_factory(ConsumableForm, extra=1)
                consumable_formset = consumable_form(initial=report.consumable_data, prefix='consumable')
                wear_form = WearForm(initial=report.wear_data)
                total_price_report = report.total_report_cost

            template = 'makereport/edit_repor.html'
            all_reports = Report.objects.all()
            if all_reports:
                report_number = Report.objects.filter(report_id=id).last()
            else:
                report_number = 1
        else:
            print('get method without id')
            image_form = ImageForm(instance=Images())
            passphoto_form = PPhotoForm(instance=PassportPhotos())
            otherphoto_form = OPhotoForm(instance=OtherPhotos())
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
            'total_price_report': total_price_report,
            'report_rate_price': request.user.myuser.report_rate_price,
            'image_form': image_form or None,
            'passphoto_form': passphoto_form or None,
            'otherphoto_form': otherphoto_form or None,
            'images': images or None,
            'pphotos': pphotos or None,
            'ophotos': ophotos or None,
        }
        return render(request, template, context)

    @method_decorator(decorators)
    def post(self, request, id=None, extend=0):
        total_report_price = 0
        if id:
            print('getting id')
            return self.put(request, id)
        report_form = ReportForm(request.POST, instance=Report())
        image_form = ImageForm(request.POST, request.FILES)
        passphoto_form = PPhotoForm(request.POST, request.FILES)
        otherphoto_form = OPhotoForm(request.POST, request.FILES)
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
        print('forms validation next')
        print(image_form.is_valid())
        print(image_form.errors)
        print(report_form.errors)
        print(car_form.errors)
        print(customer_form.errors)
        if report_form.is_valid() and car_form.is_valid() and customer_form.is_valid() and image_form.is_valid():
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
            new_report.created_by = request.user.myuser
            new_report.save()
            save_path = str(s.MEDIA_ROOT + "/")
            for each in request.FILES.getlist('image'):
                Images.objects.create(image=each, report=new_report)
                with open(save_path + each.name, 'wb+') as destination:
                    for chunk in request.FILES['image'].chunks():
                        destination.write(chunk)
            for each in request.FILES.getlist('photo'):
                PassportPhotos.objects.create(photo=each, report=new_report)
                with open(save_path + each.name, 'wb+') as destination:
                    for chunk in request.FILES['photo'].chunks():
                        destination.write(chunk)
            for each in request.FILES.getlist('photos'):
                OtherPhotos.objects.create(photos=each, report=new_report)
                with open(save_path + each.name, 'wb+') as destination:
                    for chunk in request.FILES['photos'].chunks():
                        destination.write(chunk)
            new_report.service_data = []
            new_report.product_data = []
            new_report.consumable_data = []
            new_report.wear_data = {}
            for form in service_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    print('service form is validated')
                    # new_report.service_data = []
                    sd = get_data_from_service_form(form)
                    add_service_to_report(new_report, sd.__getitem__('service_id'), sd.__getitem__('service_cost'))
                    new_report.service_data.append(sd)
                print(new_report.service_data)
            for form in product_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    print('product form is validated')
                    pd = get_data_from_product_form(form)
                    add_product_to_report(new_report, pd.__getitem__('product_id'), pd.__getitem__('product_cost'))
                    new_report.product_data.append(pd)
                print(new_report.product_data)
            for form in consumable_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    print('consum form is validated')
                    cd = get_data_from_consum_form(form)
                    add_consumable_to_report(new_report, cd.__getitem__('consumable_id'),
                                             cd.__getitem__('consumable_cost'))
                    new_report.consumable_data.append(cd)
                print(new_report.consumable_data)
            if wear_form.is_valid():
                print('wear form is validated')
                wd = get_data_from_wear_form(wear_form)
                new_report.wear_data.update(wd)
                new_report.get_total_report_price()
            new_report.set_private_key()
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
            # 'uploaded_file_url': uploaded_file_url,
        }
        return render(request, 'makereport/add_repor.html', context)

    @method_decorator(decorators)
    def put(self, request, id=None):
        report = Report.objects.get(report_id=id)
        contract = Contract.objects.get(contract_id=report.contract_id)
        image_form = ImageForm(request.POST, request.FILES)
        passphoto_form = PPhotoForm(request.POST, request.FILES)
        otherphoto_form = OPhotoForm(request.POST, request.FILES)
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
        all_reports = Report.objects.all()
        if all_reports:
            report_number = Report.objects.get(report_id=id)
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
            new_report.created_by = request.user.myuser
            new_report.save()
            save_path = str(s.MEDIA_ROOT + "/")
            print(request.FILES)
            for each in request.FILES.getlist('image'):
                Images.objects.create(image=each, report=new_report)
                with open(save_path + each.name, 'wb+') as destination:
                    for chunk in request.FILES['image'].chunks():
                        destination.write(chunk)
            for form in service_formset.forms:
                print(form.is_valid())
                if form.is_valid():
                    print('service form is validated')
                    sd = get_data_from_service_form(form)
                    add_service_to_report(new_report, sd.__getitem__('service_id'), sd.__getitem__('service_cost'))
                    new_report.service_data.append(sd)
                print(new_report.service_cost)
            for form in product_formset.forms:
                if form.is_valid():
                    print('product form is validated')
                    pd = get_data_from_product_form(form)
                    add_product_to_report(new_report, pd.__getitem__('product_id'), pd.__getitem__('product_cost'))
                    new_report.product_data.append(pd)
                print(new_report.product_cost)
            for form in consumable_formset.forms:
                if form.is_valid():
                    print('consum form is validated')
                    cd = get_data_from_consum_form(form)
                    add_consumable_to_report(new_report, cd.__getitem__('consumable_id'),
                                             cd.__getitem__('consumable_cost'))
                    new_report.consumable_data.append(cd)
                print(new_report.consumable_cost)
            if wear_form.is_valid():
                print('wear form is validated')
                wd = get_data_from_wear_form(wear_form)
                new_report.wear_data.update(wd)
                new_report.get_total_report_price()
            new_report.save()
            return HttpResponseRedirect('/report/list')
        context = {
            'report_form': report_form,
            'car_form': car_form,
            'customer_form': customer_form,
            'report_number': report_number,
            'image_form': image_form,
            'passphoto_form':passphoto_form,
            'otherphoto_form':otherphoto_form,
            'service_formset': service_formset,
            'product_formset': product_formset,
            'consumable_formset': consumable_formset,
            'wear_form': wear_form,
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
        # request.POST,
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


class UserSettingsView(View):
    decorators = [login_required]

    @method_decorator(decorators)
    def get(self, request):
        user = request.user.myuser
        report_rate_form = ReportRateSettingForm(instance=user)
        context = {
            'user': user,
            'report_rate_form': report_rate_form,
        }
        return render(request, 'makereport/user_settings.html', context)

    def post(self, request):
        user = request.user.myuser
        report_rate_form = ReportRateSettingForm(request.POST, instance=user)
        if report_rate_form.is_valid():
            print('user settings forms is valid')
            user = report_rate_form.save()

        context = {
            'user': user,
            'report_rate_form': report_rate_form,
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
            context["error"] = "Invalid data"
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


def get_sign(request):
    return render(request, 'makereport/imzo.html')


class ImageInputViem(View):
    def get(self, request, id):
        report = Report.objects.get(report_id=id)
        context = {
            'report': report,
        }
        return render(request, 'input_test.html', context)

    def post(self, request, id):
        myfiles = request.FILES['input']
        fs = FileSystemStorage()
        filename = fs.save(myfiles.name, myfiles)
        uploaded_file_url = fs.url(filename)
        return


@ensure_csrf_cookie
def test_input(request):
    report = Report.objects.get(report_id=1)
    url = s.ALLOWED_HOSTS.__getitem__(1).translate({39: None})
    # u = str("http://") + str(url) + str(report.media_photo.image.url)
    # print(u)
    # print(report.media_photo.url)
    if request.method == "POST":
        print(request.FILES['input'])
        myfiles = request.FILES['input']
        fs = FileSystemStorage()
        filename = fs.save(myfiles.name, myfiles)
        uploaded_file_url = fs.url(filename)
        return render(request, 'input_test.html', {
            'uploaded_file_url': uploaded_file_url,
            'report': report,
            # 'u': u,
        })
    return render(request, 'input_test.html', {
        'report': report,
        # 'u': u,
    })


@ensure_csrf_cookie
def delete_image(request):
    print('sadasdasdasdasd')
    print(request)
    return render(request,'input_test.html',context={'delete': True})


def search(request):
    return render(request, "makereport/auth/search.html")
