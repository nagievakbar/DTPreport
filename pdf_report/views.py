from django.http import FileResponse
from django.views.generic import View
import os
from DTPreport import settings as s
from makereport.models import Report, Images , Documents ,PassportPhotos ,OtherPhotos ,Checks
from pdf_report.utils import PyPDFML
from fpdf import FPDF
from django.core.files.base import ContentFile
import locale
import base64
from django.shortcuts import render

def get_base_template(request):
    filename = 'example.xml'
    response = FileResponse(open(os.path.join(s.MEDIA_ROOT, '../templates/{}'.format(filename)), 'rb'), content_type='text/xml')
    content = "attachment; filename=%s" % filename
    response['Content-Disposition'] = content
    return response
    
class GeneratePDF(View):
    def get(self, request, id=id):
        get_response(request, id)
        report_pdf = Report.objects.get(report_id=id)
 
        # filename = "%s.pdf" % report_pdf.car.car_number
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
        images = Images.objects.filter(report_id=id)
        passport = PassportPhotos.objects.filter(report_id = id)
        checks = Checks.objects.filter(report_id = id)
        other_photos = OtherPhotos.objects.filter(report_id = id)
        file = request.user.myuser.template
        documnet_photo = Documents.objects.first()
        path_for_images = s.MEDIA_ROOT
        print(images)
        if file != None:
            splited = file.name.split('/')
            path = os.path.join(s.MEDIA_ROOT,"{}".format(splited[0]))
            print("path_for_images {}".format(path_for_images))
            print("path {}".format(path))
            pdf = PyPDFML(splited[-1],path)
        else:
            pdf = PyPDFML('example.xml')
        image_variable = 0;
        context = {
            'report': new_report_pdf,
            'services': new_report_pdf.service.all().__len__(),
            'datetime': new_report_pdf.report_date,
            'qrcode': new_report_pdf.pdf_qr_code_user,
            'qrcode_admin':new_report_pdf.pdf_qr_code_admin,
            'images': images,
            'documnet_photo':documnet_photo,
            'passport':passport,
            'checks': checks,
            'other_photos':other_photos,
            }
        pdf.generate(context)
        data = pdf.contents()
        filename = "%s.pdf" % new_report_pdf.car.car_number
        new_report_pdf.pdf_report.save(filename, ContentFile(data))
        with open(new_report_pdf.pdf_report.path, "rb") as file:
            encoded_string = base64.b64encode(file.read())
        new_report_pdf.pdf_report_base64 = encoded_string.decode('ascii')
        print( new_report_pdf.pdf_report_base64[0:10])
        new_report_pdf.save()

def create_base64(request, new_report_pdf):
        locale.setlocale(locale.LC_ALL, 'C')
        file = request.user.myuser.template
        if file != None:
            splited = file.name.split('/')
            path = os.path.join(s.MEDIA_ROOT,"{}".format(splited[0]))
            pdf = PyPDFML(splited[-1],path)
        else:
            pdf = PyPDFML('example.xml')
        image_variable = 0;
        
        context = {
            'report': new_report_pdf,
            'services': new_report_pdf.service.all().__len__(),
            'datetime': new_report_pdf.report_date,
            'qrcode': new_report_pdf.pdf_qr_code_user,
            'qrcode_admin':new_report_pdf.pdf_qr_code_admin,
            'images': "",
            'documnet_photo':"",
            'passport':"",
            'checks': "",
            'other_photos':"",
            }

        pdf.generate(context)
        data = pdf.contents()
        filename = "%s.pdf" % new_report_pdf.car.car_number
        new_report_pdf.pdf_report.save(filename, ContentFile(data))
        with open(new_report_pdf.pdf_report.path, "rb") as file:
            encoded_string = base64.b64encode(file.read())
        new_report_pdf.pdf_report_base64 = encoded_string.decode('ascii')

        new_report_pdf.save()