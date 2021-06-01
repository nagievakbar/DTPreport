from django.http import FileResponse, JsonResponse
from django.views.generic import View
import os
from DTPreport import settings as s
from makereport.models import Report, Documents, Contract, Calculation, \
    HoldsImages, TemplateBase, TemplateMixing, TemplateAgreement, TemplateAdditional
from pdf_report.utils import PyPDFML, generate_pdf

from django.core.files.base import ContentFile

import locale
import base64
import jinja2


def get_base_additional_template(request):
    file = TemplateAdditional.objects.last().template
    name = 'example.xml'
    return handle_schema(file=file, default_name=name)


def get_base_template(request):
    file = TemplateBase.objects.last().template
    name = 'example.xml'
    return handle_schema(file=file, default_name=name)


def get_base_mixing_template(request):
    file = TemplateMixing.objects.last().template
    name = 'mixing.xml'
    return handle_schema(file=file, default_name=name)


def get_base_agreement_template(request):
    name = 'agreem.xml'
    file = TemplateAgreement.objects.last().template
    return handle_schema(file=file, default_name=name)


def handle_schema(file, default_name):
    try:
        file_data = open(file.path, 'rb')
        return get_file(file=file_data, name=file.name)
    except:
        print(default_name)
        file_data = open(os.path.join(s.MEDIA_ROOT, '../templates/{}'.format(default_name)), 'rb')
        return get_file(file=file_data, name=default_name)


def get_file(file, name, content_type='text/xml'):
    response = FileResponse(file,
                            content_type=content_type)
    content = "attachment; filename=%s" % name
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
            'qrcode': get_qrc_code(qr_company=report.pdf_qr_code_company, qr_user=report.pdf_qr_code_user),
            'contract': contract,
        }
        try:
            file = TemplateMixing.objects.last().template
            print("asdsad")
            print(file)
            splited = file.name.split('/')
            print(splited)
            path = os.path.join(s.MEDIA_ROOT, "{}".format(splited[0]))
            pdf = PyPDFML(splited[-1], path)
            pdf.generate(context)
        except (jinja2.exceptions.TemplateNotFound, AttributeError):
            pdf = PyPDFML('mixing.xml')
            print("ERROR OCCURED")
            pdf.generate(context)
        data = pdf.contents()
        response = FileResponse(ContentFile(data), content_type='application/pdf')
        return response


from flask_qrcode import QRcode

def check_qr_code(qrcode:str) :
    return  QRcode.qrcode(qrcode) if qrcode is not None else None

def test_api(request, id):
    report = Report.objects.get(report_id=id)
    car = report.car
    contract = report.contract
    customer = contract.customer
    qrcode = get_qrc_code(qr_company="SAdasdasdsaasdsadsa", qr_user=report.pdf_qr_code_user)
    context = {
        'car': car,
        'customer': customer,
        'report': report,
        'qrcode': check_qr_code(qrcode),
        'contract': contract,
        'qrcode_some': QRcode.qrcode("http://e-otsenka.uz/pdf/{id}".format(id=report.report_id))
    }
    pdf = generate_pdf(html_name="finishing_report.html", css_name="finish_report.css", context=context)
    reponse = FileResponse(ContentFile(pdf), content_type='application/pdf')
    return reponse


def test_agreement(request, id):
    report = Report.objects.get(report_id=id)
    calculation = Calculation.objects.get(report_id=id)
    contract = report.contract
    context = {
        'calculation': calculation,
        'report': report,
        'qrcode': check_qr_code("Asdsadasdasdsadasdasdsadsadsadasdasd sadas"),
        'contract': contract,
    }
    pdf = generate_pdf(context=context, html_name="aggreement_report.html", css_name='aggreement_report.css')
    response = FileResponse(ContentFile(pdf), content_type='application/pdf')
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
            'qrcode': report.pdf_qr_code_company,
            'contract': contract,
        }
        try:
            file = TemplateAgreement.objects.last().template
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


def get_qrc_code(qr_company, qr_user):
    if (qr_company is not None and qr_user is not None) and (qr_company != "" and qr_user != ""):
        return "{company} {user}".format(company=qr_company, user=qr_user)
    elif qr_company is not None and qr_company != "":
        return qr_company
    elif qr_user is not None and qr_user != "":
        return qr_user
    return None


class GenerateAdditional(View):
    def get(self, request, id=None):
        if id == 0:
            return get_file('base.pdf', content_type='application/pdf')
        data = get_additional(request, id)
        response = FileResponse(ContentFile(data), content_type='application/pdf')
        return response


class GeneratePDF(View):
    def get(self, request, id=None):
        if type(id) is not int or id <= 0:
            return get_file('base.pdf', content_type='application/pdf')
        get_bases(id)
        report_pdf = Report.objects.get(report_id=id)
        response = FileResponse(open(os.path.join(report_pdf.pdf_report.path), 'rb'), content_type='application/pdf')
        content = "attachment; filename='%s'" % report_pdf.pdf_report.name + ".pdf"
        #         response['Content-Disposition'] = content
        return response


def get_bases(id):
    obj = TemplateBase.objects
    new_report_pdf = Report.objects.get(report_id=id)
    data = get_response(id, obj=obj)
    filename = "%s.pdf" % new_report_pdf.car.car_number
    new_report_pdf.pdf_report.save(filename, ContentFile(data))
    new_report_pdf.save()


def get_additional(request, id):
    obj = TemplateAdditional.objects
    return get_response(id, obj=obj)


def get_response(id, obj):
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
        'qrcode_company': new_report_pdf.pdf_qr_code_company,
        'images': images,
        'document_photo': document_photo,
        'passport': passport,
        'checks': checks,
        'other_photos': other_photos,
    }
    try:
        file = obj.last().template
        splited = file.name.split('/')
        path = os.path.join(s.MEDIA_ROOT, "{}".format(splited[0]))
        pdf = PyPDFML(splited[-1], path)
        pdf.generate(context)
    except (jinja2.exceptions.TemplateNotFound, AttributeError):
        pdf = PyPDFML('example.xml')
        pdf.generate(context)
    return pdf.contents()


def create_base64(request, new_report_pdf):
    locale.setlocale(locale.LC_ALL, 'C')
    calculation = Calculation.objects.create()
    context = {
        'calculation': calculation,
        'contract': new_report_pdf.contract,
        'report': new_report_pdf,
        'services': new_report_pdf.service.all().__len__(),
        'datetime': new_report_pdf.report_date,
        'qrcode': new_report_pdf.pdf_qr_code_user,
        'qrcode_admin': new_report_pdf.pdf_qr_code_company,
        'images': "",
        'document_photo': "",
        'passport': "",
        'checks': "",
        'other_photos': "",
    }
    try:
        file = TemplateBase.objects.last().template
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
