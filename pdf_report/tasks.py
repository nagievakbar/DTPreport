from celery import shared_task
from django.core.files.base import ContentFile
from django.http import JsonResponse
from PIL import Image
from pdf_report.views import get_response, test_report_base
from django.db.models import Q
from makereport.models import TemplateBase, Report, Images, TemplateAdditional


@shared_task(name="reduce_image")
def reduce_image(path):
    image_opened = Image.open(path)
    width, height = image_opened.size
    image_opened = image_opened.resize((int(width / 2), int(height / 2)), Image.ANTIALIAS)
    image_opened.save(path, quality=10)


def get_base(request):
    try:
        id = request.GET.get('id', 0)
        make_pdf.delay(id)
    except Report.DoesNotExist:
        pass
    return JsonResponse({})


def get_additional_pdf(request):
    try:
        id = request.GET.get('id', 0)
        make_pdf_additional.delay(id)
    except Report.DoesNotExist:
        pass
    return JsonResponse({})


@shared_task(name="delete_empty")
def delete_empty_report():
    report = Report.objects.filter((Q(key__isnull=True) | Q(key__exact='')))
    for rep in report.all():
        rep.delete()


@shared_task(name="make_pdf")
def make_pdf(id):
    obj = TemplateBase
    new_report_pdf = Report.objects.get(report_id=id)
    data = test_report_base(id, obj=obj)
    filename = "%s.pdf" % new_report_pdf.car.car_number
    new_report_pdf.save_pdf(filename, data)


@shared_task(name="make_pdf_additional")
def make_pdf_additional(id):
    obj = TemplateAdditional
    new_report_pdf = Report.objects.get(report_id=id)
    data = test_report_base(id, obj=obj)
    filename = "%s.pdf" % new_report_pdf.car.car_number
    new_report_pdf.save_additional_pdf(filename, data)
