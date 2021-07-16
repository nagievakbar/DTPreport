from datetime import datetime
from io import BytesIO

import PyPDF2
from django.core.files.base import ContentFile

from makereport.models import Disposable


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
        pdf_first = open(self.disposable_model.pdf_disposable.path, 'rb')
        pdf_first_reader = PyPDF2.PdfFileReader(pdf_first)
        number_of_pages = pdf_first_reader.numPages
        self._write(pdf_first_reader)
        pdf_first.close()
        return number_of_pages

    def _write(self, reader: PyPDF2.PdfFileReader):
        for page_num in range(reader.numPages):
            page_obj = reader.getPage(page_num)
            self.pdf_writer.addPage(page_obj)

    def create_second_pdf(self, number_pages: int) -> ContentFile:
        context = {
            'number_of_pages': number_pages
        }
        from pdf_report.utils import generate_pdf
        pdf = generate_pdf(context=context, default_template="report.html",
                           css_name="report.css")
        return ContentFile(pdf)

    def write_second_pdf(self, pdf_second: ContentFile):
        pdf_second_reader = PyPDF2.PdfFileReader(pdf_second)
        self._write(pdf_second_reader)
        pdf_second.close()

    def store_pdf(self):
        pdf_output = BytesIO()
        self.pdf_writer.write(pdf_output)
        filename = "created_{}_{}".format(datetime.now().timestamp(), self.disposable_model.id)
        self.disposable_model.save_created_pdf(filename, pdf_output)
        pdf_output.close()
