from django.http import FileResponse
from django.views.generic import View
import os
from DTPreport import settings as s
from makereport.models import Report
from pdf_report.utils import PyPDFML
from django.core.files.base import ContentFile
import locale


class GeneratePDF(View):
    def get(self, request, id=id):
        locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")

        new_report_pdf = Report.objects.get(report_id=id)
        pdf = PyPDFML('example.xml')
        context = {
            'report': new_report_pdf,
            'datetime': str(new_report_pdf.created_at.strftime((" «%d»  %b  %Yг. ")))
        }
        pdf.generate(context)
        data = pdf.contents()

        filename = "%s.pdf" % new_report_pdf.car.car_number

        new_report_pdf.pdf_report.save(filename, ContentFile(data))

        return get_response(request, new_report_pdf.report_id)


def get_response(request, id):
    report_pdf = Report.objects.get(report_id=id)
    filename = "%s.pdf" % report_pdf.car.car_number
    response = FileResponse(open(os.path.join(s.MEDIA_ROOT, filename), 'rb'), content_type='application/pdf')
    content = "inline; filename=%s" % filename
    download = request.GET.get("download")
    if download:
        content = "attachment; filename='%s'" % filename
    response['Content-Disposition'] = content
    return response


