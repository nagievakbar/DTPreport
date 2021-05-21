from celery import shared_task
from django.core.files.base import ContentFile
from django.http import JsonResponse
from PIL import Image
from pdf_report.views import get_response
from django.db.models import Q
from makereport.models import TemplateBase, Report, Images


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


@shared_task(name="delete_empty")
def delete_empty_report():
    report = Report.objects.filter((Q(key__isnull=True) | Q(key__exact='')))
    for rep in report.all():
        rep.delete()


@shared_task(name="make_pdf")
def make_pdf(id):
    obj = TemplateBase.objects
    new_report_pdf = Report.objects.get(report_id=id)
    data = get_response(id, obj=obj)
    filename = "%s.pdf" % new_report_pdf.car.car_number
    new_report_pdf.pdf_report.save(filename, ContentFile(data))
    new_report_pdf.save()
