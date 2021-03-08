from django.http import FileResponse
from django.views.generic import View
import os
from DTPreport import settings as s
from makereport.models import Report, Images
from pdf_report.utils import PyPDFML
from fpdf import FPDF
from django.core.files.base import ContentFile
import locale
import base64
from django.shortcuts import render


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
        pdf = PyPDFML('example.xml')
        context = {
            'report': new_report_pdf,
            'services': new_report_pdf.service.all().__len__(),
            'images': images,
            'datetime': new_report_pdf.report_date,
            'qrcode': new_report_pdf.pdf_qr_code
        }
        pdf.generate(context)
        data = pdf.contents()
        filename = "%s.pdf" % new_report_pdf.car.car_number
        new_report_pdf.pdf_report.save(filename, ContentFile(data))
        with open(new_report_pdf.pdf_report.path, "rb") as file:
            encoded_string = base64.b64encode(file.read())
        new_report_pdf.pdf_report_base64 = encoded_string

        new_report_pdf.save()