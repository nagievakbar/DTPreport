from celery import shared_task
from django.core.files.base import ContentFile
from django.http import JsonResponse
from PIL import Image
from pdf_report.views import get_response, generate_pdf_report, generate_pdf_enumeration
from django.db.models import Q
from makereport.models import TemplateBase, Report, Images, TemplateAdditional, Enumeration, Disposable


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
    data = generate_pdf_report(id, obj=obj)
    filename = "main_{}.pdf".format(new_report_pdf.report_id)
    new_report_pdf.save_pdf(filename, data)


@shared_task(name="make_pdf_additional")
def make_pdf_additional(id):
    obj = TemplateAdditional
    new_report_pdf = Report.objects.get(report_id=id)
    data = generate_pdf_report(id, obj=obj)
    filename = "second_{}.pdf".format(new_report_pdf.report_id)
    new_report_pdf.save_additional_pdf(filename, data)


@shared_task(name="make_pdf_enumeration")
def make_pdf_enumeration(id):
    obj = TemplateBase
    new_report_pdf = Enumeration.objects.get(report_id=id)
    data = generate_pdf_enumeration(id, obj=obj)
    filename = "main_enumeration_{}.pdf".format(new_report_pdf.report_id)
    new_report_pdf.save_pdf_enumeration(filename, data)


@shared_task(name='concatenate_pdf_disposable')
def concatenate_pdf_disposable(id: int):
    manger = PDFMerger(id)
    manger.concatenate_pdf()


import PyPDF2

from io import BytesIO


class PDFMerger:
    def __init__(self, id: int):
        self.disposable_model = Disposable.objects.get(id=id)
        self.pdf_writer = PyPDF2.PdfFileWriter()

    def concatenate_pdf(self):
        number_pages = self.write_first_pdf()
        pdf_second = self.create_second_pdf(number_pages)
        self.write_second_pdf(pdf_second)
        self.store_pdf()

    # I will use pdf writer for creating merged pdf
    def write_first_pdf(self) -> int:
        pass

    def create_second_pdf(self, number_pages: int) -> bytes:
        pass

    def write_second_pdf(self, pdf_second: bytes):
        pass

    def store_pdf(self):
        pass

    def test_method(self):
        # Open the files that have to be merged one by one
        pdf1File = open('FirstInputFile.pdf', 'rb')
        pdf2File = open('SecondInputFile.pdf', 'rb')

        # Read the files that you have opened
        pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
        pdf2Reader = PyPDF2.PdfFileReader(pdf2File)

        # Create a new PdfFileWriter object which represents a blank PDF document
        pdfWriter = PyPDF2.PdfFileWriter()

        # Loop through all the pagenumbers for the first document
        for pageNum in range(pdf1Reader.numPages):
            pageObj = pdf1Reader.getPage(pageNum)
            pdfWriter.addPage(pageObj)

        # Loop through all the pagenumbers for the second document
        for pageNum in range(pdf2Reader.numPages):
            pageObj = pdf2Reader.getPage(pageNum)
            pdfWriter.addPage(pageObj)

        # Now that you have copied all the pages in both the documents, write them into the a new document
        pdfOutputFile = BytesIO()
        pdfWriter.write(pdfOutputFile)
        # Close all the files - Created as well as opened
        pdfOutputFile.close()
        pdf1File.close()
        pdf2File.close()
