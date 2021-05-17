from celery import shared_task
from django.core.files.base import ContentFile
from pdf_report.views import get_response

from makereport.models import TemplateBase, Report


@shared_task(name="make_pdf")
def make_pdf(id):
    obj = TemplateBase.objects
    new_report_pdf = Report.objects.get(report_id=id)
    data = get_response(id, obj=obj)
    filename = "%s.pdf" % new_report_pdf.car.car_number
    new_report_pdf.pdf_report.save(filename, ContentFile(data))
    new_report_pdf.save()
