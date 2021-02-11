from django.http import FileResponse
from django.views.generic import View
import os
from DTPreport import settings as s
from makereport.models import Report
from pdf_report.utils import PyPDFML
from fpdf import FPDF
from django.core.files.base import ContentFile
import locale
from django.shortcuts import render


class GeneratePDF(View):
    def get(self, request, id):
        pdf = FPDF()
        pdf.set_title('Title')
        pdf.set_left_margin(15)
        pdf.set_right_margin(15)
        pdf.add_page()
        pdf.add_font("Arial", 'I', 'static/makereport/fonts/Arial.ttf', uni=True)
        pdf.add_font("Arial", 'B', 'static/makereport/fonts/Arial Bold.ttf', uni=True)
        pdf.set_font("Arial", 'I', size=10)
        text = "    Welcome to Python Welcome to Python Welcome to Python Welcome to Python Welcome to Python Welcome to Python Welcome to Python Welcome to Python Welcome to Python Welcome to Python Welcome to Python"
        text2 = "   Welcome to 2222 Welcome to 2222 Welcome to 2222Welcome to 2222Welcome to 2222Welcome to 2222Welcome to 2222Welcome to 2222Welcome to 2222Welcome to 2222Welcome to 2222Welcome to 2222 "
        data = [text, text2]
        image_path = os.path.join(s.STATIC_ROOT, 'makereport/img/Logo.jpg')
        pdf.set_x(15)
        pdf.image(image_path, h=35, w=60)
        pdf.set_xy(x=90, y=20)
        pdf.cell(100, txt='ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ', align="R")
        pdf.set_xy(x=90, y=25)
        pdf.cell(100, txt='«AMIR AVTO BAHOLASH»', align='R')
        pdf.line(15, 45, 190, 45)
        pdf.line(15, 46, 190, 46)
        pdf.set_line_width(1)
        pdf.set_draw_color(255, 0, 0)
        pdf.set_xy(x=10, y=50)
        pdf.multi_cell(180, 5, txt=""" г.Ташкент ул. Бунедкор 118, тел.: 279-46-60, факс: 279-33-38, МФО 01067
    р/с: 20208000200244206001   Чиланзарский ф-л ОАИКБ «Ипак Йули», ИНН 302 667624 ОКОНХ 84500""", align='C')
        pdf.set_xy(120, 65)
        pdf.cell(40, txt='г-же Курбановой О.Т.', align='R')
        pdf.ln(10)
        pdf.set_font('Arial', 'B', size=10)
        pdf.cell(180, txt='Уважаемая Одина Тохировна', align='C')
        pdf.ln(10)
        pdf.set_font('Arial', 'I', size=10)
        report_id = Report.objects.get(report_id=id).report_id
        txt22 = """ В соответствии с Договором об оценке имущества № {} """.format(report_id)
        pdf.multi_cell(190, 5, txt=txt22, align="J", border=0)
        # for each in data:
        #     pdf.multi_cell(190, 5, txt=each, align="J", border=0)
        pdf.output("simple_dedmo.pdf")
        return FileResponse(open("simple_dedmo.pdf", 'rb'))



#
# class GeneratePDF(View):
#     def get(self, request, id=id):
#         locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
#
#         new_report_pdf = Report.objects.get(report_id=id)
#         pdf = PyPDFML('example.xml')
#         context = {
#             'report': new_report_pdf,
#             'services': new_report_pdf.service.all().__len__(),
#             'datetime': str(new_report_pdf.created_at.strftime((" «%d»  %b  %Yг. ")))
#         }
#         pdf.generate(context)
#         data = pdf.contents()
#
#         filename = "%s.pdf" % new_report_pdf.car.car_number
#
#         new_report_pdf.pdf_report.save(filename, ContentFile(data))
#
#         return get_response(request, new_report_pdf.report_id)
#
#
# def get_response(request, id):
#     report_pdf = Report.objects.get(report_id=id)
#     # filename = "%s.pdf" % report_pdf.car.car_number
#     filename = str(report_pdf.pdf_report)
#     response = FileResponse(open(os.path.join(s.MEDIA_ROOT, filename), 'rb'), content_type='application/pdf')
#     content = "inline; filename=%s" % filename
#     download = request.GET.get("download")
#     if download:
#         content = "attachment; filename='%s'" % filename
#     response['Content-Disposition'] = content
#     return response
