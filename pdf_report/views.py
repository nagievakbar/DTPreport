from django.http import FileResponse, JsonResponse
from django.views.generic import View
import os
from DTPreport import settings as s
from makereport.models import Report, Documents, Contract, Calculation, \
    HoldsImages
from pdf_report.utils import PyPDFML
from fpdf import FPDF
from django.core.files.base import ContentFile
import locale
import base64
import jinja2


def get_base_template(request):
    filename = 'example.xml'
    return get_file(filename)


def get_base_mixing_template(request):
    filename = 'mixing.xml'
    return get_file(filename)


def get_base_agreement_template(request):
    filename = 'agreem.xml'
    return get_file(filename)


def get_file(filename, content_type='text/xml'):
    response = FileResponse(open(os.path.join(s.MEDIA_ROOT, '../templates/{}'.format(filename)), 'rb'),
                            content_type=content_type)
    content = "attachment; filename=%s" % filename
    response['Content-Disposition'] = content
    return response


class GenerateMixing(View):
    def get(self, request, id=None):
        if id == 0:
            return get_file('mixing.pdf', content_type='application/pdf')
        report = Report.objects.get(report_id=id)
        car = report.car
        contract = report.contract
        customer = contract.customer
        context = {
            'car': car,
            'customer': customer,
            'report': report,
            'contract': contract,
        }
        try:
            file = request.user.myuser.template_mixing
            splited = file.name.split('/')
            path = os.path.join(s.MEDIA_ROOT, "{}".format(splited[0]))
            pdf = PyPDFML(splited[-1], path)
            pdf.generate(context)
        except (jinja2.exceptions.TemplateNotFound, AttributeError):
            pdf = PyPDFML('mixing.xml')
            pdf.generate(context)
        data = pdf.contents()
        response = FileResponse(ContentFile(data), content_type='application/pdf')
        return response


class GenerateAgreement(View):
    def get(self, request, id=None):
        if id == 0:
            return get_file('agreement.pdf', content_type='application/pdf')
        report = Report.objects.get(report_id=id)
        calculation = Calculation.objects.get(report_id=id)
        contract = report.contract
        context = {
            'calculation': calculation,
            'report': report,
            'contract': contract,
        }
        try:
            file = request.user.myuser.template_agreement
            splited = file.name.split('/')
            path = os.path.join(s.MEDIA_ROOT, "{}".format(splited[0]))
            pdf = PyPDFML(splited[-1], path)
            pdf.generate(context)
        except (jinja2.exceptions.TemplateNotFound, AttributeError):
            pdf = PyPDFML('agreem.xml')
            pdf.generate(context)

        data = pdf.contents()
        response = FileResponse(ContentFile(data), content_type='application/pdf')
        return response


class GeneratePDF(View):
    def get(self, request,  id=None):
        if type(id) is not int or id <= 0:
            return get_file('base.pdf', content_type='application/pdf')
        get_response(request, id)
        report_pdf = Report.objects.get(report_id=id)

        filename = str(report_pdf.pdf_report)

        response = FileResponse(open(os.path.join(s.MEDIA_ROOT, filename), 'rb'), content_type='application/pdf')
        content = "inline; filename=%s" % filename
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % filename
        response['Content-Disposition'] = content
        return response


def get_response(request, id):
    locale.setlocale(locale.LC_ALL, 'C')
    new_report_pdf = Report.objects.get(report_id=id)
    calculation = Calculation.objects.get(report_id=id)
    contract = Contract.objects.get(contract_id=new_report_pdf.contract_id)
    holds_images = HoldsImages.objects.get(report_id=id)
    images = holds_images.image.all()
    passport = holds_images.pp_photo.all()
    checks = holds_images.checks.first()
    other_photos = holds_images.o_images.all()
    document_photo = Documents.objects.first()
    path_for_images = s.MEDIA_ROOT
    context = {
        'calculation': calculation,
        'contract': contract,
        'report': new_report_pdf,
        'services': new_report_pdf.service.all().__len__(),
        'datetime': new_report_pdf.report_date,
        'qrcode': new_report_pdf.pdf_qr_code_user,
        'qrcode_admin': new_report_pdf.pdf_qr_code_admin,
        'images': images,
        'document_photo': document_photo,
        'passport': passport,
        'checks': checks,
        'other_photos': other_photos,
    }
    try:
        file = request.user.myuser.template
        splited = file.name.split('/')
        path = os.path.join(s.MEDIA_ROOT, "{}".format(splited[0]))
        pdf = PyPDFML(splited[-1], path)
        pdf.generate(context)
    except (jinja2.exceptions.TemplateNotFound, AttributeError):
        pdf = PyPDFML('example.xml')
        pdf.generate(context)
    data = pdf.contents()
    filename = "%s.pdf" % new_report_pdf.car.car_number
    new_report_pdf.pdf_report.save(filename, ContentFile(data))
    new_report_pdf.save()


def create_base64(request, new_report_pdf):
    locale.setlocale(locale.LC_ALL, 'C')
    context = {
        'calculation': "",
        'contract': "",
        'report': new_report_pdf,
        'services': new_report_pdf.service.all().__len__(),
        'datetime': new_report_pdf.report_date,
        'qrcode': new_report_pdf.pdf_qr_code_user,
        'qrcode_admin': new_report_pdf.pdf_qr_code_admin,
        'images': "",
        'document_photo': "",
        'passport': "",
        'checks': "",
        'other_photos': "",
    }
    try:
        file = request.user.myuser.template
        splited = file.name.split('/')
        path = os.path.join(s.MEDIA_ROOT, "{}".format(splited[0]))
        pdf = PyPDFML(splited[-1], path)
        pdf.generate(context)
    except (jinja2.exceptions.TemplateNotFound, AttributeError):
        pdf = PyPDFML('example.xml')
        pdf.generate(context)
    data = pdf.contents()
    filename = "%s.pdf" % new_report_pdf.car.car_number
    new_report_pdf.pdf_report.save(filename, ContentFile(data))
    with open(new_report_pdf.pdf_report.path, "rb") as file:
        encoded_string = base64.b64encode(file.read())
    new_report_pdf.pdf_report_base64 = encoded_string.decode('ascii')

    new_report_pdf.save()
