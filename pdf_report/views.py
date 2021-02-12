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


# class GeneratePDF(View):
#     def get(self, request, id):
#         pdf = FPDF()
#         # ------------------------Title----------------------------------------
#         pdf.set_title('Title')
#         # ------------------------Margins--------------------------------------
#         pdf.set_left_margin(15)
#         pdf.set_right_margin(15)
#         # ------------------------Fonts----------------------------------------------
#         pdf.add_font("TNR", 'I', 'static/makereport/fonts/Times New Roman 400.ttf', uni=True)
#         pdf.add_font("TNR", 'B', 'static/makereport/fonts/Times New Roman 400 Bold.ttf', uni=True)
#         pdf.add_font("Arial", 'I', 'static/makereport/fonts/Arial.ttf', uni=True)
#         pdf.add_font("Arial", 'B', 'static/makereport/fonts/Arial Bold.ttf', uni=True)
#         # ------------------------Var----------------------------------------------
#         report = Report.objects.get(report_id=id)
#         image_path = os.path.join(s.STATIC_ROOT, 'makereport/img/Logo.jpg')
#         datetime = str(report.created_at.strftime(" «%d»  %b  %Yг. "))
#         # ------------------------Add Page------------------------------------------
#         pdf.add_page()
#         # # ------------------------Image-------------------------------------
#         # pdf.set_font("TNR", 'I', size=11)
#         # pdf.set_x(15)
#         # pdf.image(image_path, h=35, w=60)
#         # # -------------------------Text-----------------------------------------
#         # pdf.set_xy(x=90, y=25)
#         # pdf.cell(100, txt='ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ', align="R")
#         # # -------------------------Text-----------------------------------------
#         # pdf.set_font("TNR", 'I', size=20)
#         # pdf.set_xy(x=90, y=30)
#         # pdf.cell(100,10, txt='«AMIR AVTO BAHOLASH»', align='R')
#         # # --------------------------Lines----------------------------------------
#         # pdf.line(15, 45, 190, 45)
#         # pdf.line(15, 46, 190, 46)
#         # pdf.set_draw_color(255, 255, 255)
#         # pdf.set_line_width(1)
#         # # -------------------------Text-----------------------------------------
#         # pdf.set_xy(x=10, y=50)
#         # pdf.set_font('TNR', 'B', size=10)
#         # pdf.multi_cell(180, 5,
#         #                txt=""" Лицензия Госкомимущества РУз на осущестьвление оценочной деятельности серия BL 001 №0033 регистрационный №RR-0184 от 12.05.2014г.""",
#         #                align='C')
#         # # -------------------------Text-----------------------------------------
#         # pdf.set_font('TNR', 'I', size=10)
#         # pdf.set_xy(130, 65)
#         # pdf.multi_cell(w=60, h=5,
#         #                txt="""Утверждаю\nДиректор\nООО «AMIR AVTO BAHOLASH»\n_________ Сагдуллаев Б.К.\n{}""".format(
#         #                    datetime), align='C')
#         # # -------------------------Text-----------------------------------------
#         # pdf.ln(30)
#         # pdf.set_font('TNR', 'B', size=35)
#         # pdf.cell(180, txt='Отчет', align='C')
#         # # -------------------------Text-----------------------------------------
#         # pdf.ln(10)
#         # pdf.set_font('TNR', 'I', size=11)
#         # pdf.multi_cell(180, 5, txt=""" Об оценки по определению рыночной стоимости ущерба автотранспортного средства марки\n
#         #    {}, гос номер {}""".format(report.car.brand, report.car.car_number), align="C", border=0)
#         # # -------------------------Text-----------------------------------------
#         # pdf.ln(10)
#         # pdf.set_font('TNR', 'B', size=11)
#         # pdf.multi_cell(100, 5, txt='Регистрационный        {}\nномер:'.format(report.car.registration), align='L',
#         #                border=0)
#         # # -------------------------Text-----------------------------------------
#         # pdf.ln(5)
#         # pdf.multi_cell(100, 5, txt='Цель оценки:', align='L', border=0)
#         # # -------------------------Text-----------------------------------------
#         # pdf.set_font('TNR', 'I', size=11)
#         # pdf.set_xy(55, 170)
#         # pdf.multi_cell(140, 5,
#         #                txt='Определение рыночной стоимости затрат на восстановление АМТС, пострадавшего в результате ДТП',
#         #                align='L', border=0)
#         # # -------------------------Text-----------------------------------------
#         # pdf.set_font('TNR', 'B', size=11)
#         # pdf.multi_cell(w=50, h=5, txt='Назначение\nрезультатов\nоценки:', align='L')
#         # # -------------------------Text-----------------------------------------
#         # pdf.set_font('TNR', 'I', size=11)
#         # pdf.set_xy(55, 183)
#         # pdf.multi_cell(140, 5,
#         #                txt="""результаты оценки предполагается использовать в целях разрешения спора о величине причиненного имуществу ущерба.""")
#         # # -------------------------Text-----------------------------------------
#         # pdf.ln()
#         # pdf.set_font('TNR', 'B', size=11)
#         # pdf.multi_cell(w=50, h=5, txt='Место регистрации:', align='L')
#         # # -------------------------Text-----------------------------------------
#         # pdf.set_xy(55, 198)
#         # pdf.set_font('TNR', 'I', size=11)
#         # pdf.multi_cell(w=80, h=5, txt='{}'.format(report.contract.customer.address), align='L')
#         # # -------------------------Text-----------------------------------------
#         # pdf.ln()
#         # pdf.set_font('TNR', 'B', size=11)
#         # pdf.multi_cell(w=50, h=5, txt='Дата оценки:', align='L')
#         # # -------------------------Text-----------------------------------------
#         # pdf.set_xy(55, 208)
#         # pdf.set_font('TNR', 'I', size=11)
#         # pdf.multi_cell(w=80, h=5, txt='{}'.format(datetime), align='L')
#         # # -------------------------Text-----------------------------------------
#         # pdf.ln()
#         # pdf.set_font('TNR', 'B', size=11)
#         # pdf.multi_cell(w=50, h=5, txt='Дата составления\nОтчета:', align='L')
#         # # -------------------------Text-----------------------------------------
#         # pdf.set_xy(55, 220)
#         # pdf.set_font('TNR', 'I', size=11)
#         # pdf.multi_cell(w=80, h=5, txt='{}'.format(datetime), align='L')
#         # # -------------------------Text-----------------------------------------
#         # pdf.ln()
#         # pdf.set_font('TNR', 'B', size=11)
#         # pdf.multi_cell(w=50, h=5, txt='Заказчик:', align='L')
#         # # -------------------------Text-----------------------------------------
#         # pdf.set_xy(55, 230)
#         # pdf.set_font('TNR', 'I', size=11)
#         # pdf.multi_cell(w=80, h=5, txt='{}'.format(report.contract.customer.name), align='L')
#         # # -------------------------Text-----------------------------------------
#         # pdf.ln()
#         # pdf.set_font('TNR', 'B', size=11)
#         # pdf.multi_cell(w=50, h=5, txt='Собственник\nобъекта оценки:', align='L')
#         # # -------------------------Text-----------------------------------------
#         # pdf.set_xy(55, 243)
#         # pdf.set_font('TNR', 'I', size=11)
#         # pdf.multi_cell(w=80, h=5, txt='{}'.format(report.car.car_owner), align='L')
#         # # -------------------------Text-----------------------------------------
#         # pdf.ln(20)
#         # pdf.multi_cell(w=180, h=5, txt='Ташкент - {}'.format(report.created_at.strftime("%Yг.")), align='C')
#         # -------------------------New Page-----------------------------------------
#         # ------------------------Image-------------------------------------
#         pdf.set_x(15)
#         pdf.image(image_path, h=35, w=60)
#         # -------------------------Text-----------------------------------------
#         pdf.set_font("TNR", 'I', size=10)
#         pdf.set_xy(x=90, y=20)
#         pdf.cell(100, txt='ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ', align="R")
#         # -------------------------Text-----------------------------------------
#         pdf.set_xy(x=90, y=25)
#         pdf.cell(100, txt='«AMIR AVTO BAHOLASH»', align='R')
#         # --------------------------Lines----------------------------------------
#         pdf.line(15, 45, 190, 45)
#         pdf.line(15, 46, 190, 46)
#         pdf.set_draw_color(255, 255, 255)
#         pdf.set_line_width(1)
#         # -------------------------Text-----------------------------------------
#         pdf.set_xy(15,50)
#         pdf.multi_cell(180,5,txt=""" г.Ташкент ул. Бунедкор 118, тел.: 279-46-60, факс: 279-33-38, МФО 01067\nр/с: 20208000200244206001  Чиланзарский ф-л ОАИКБ «Ипак Йули», ИНН 302 667624 ОКЭД 68310""", align='C')
#         # -------------------------Text-----------------------------------------
#         pdf.set_xy(15, 60)
#         pdf.multi_cell(170, 5, txt="г-ну {}".format(report.contract.customer.name), align='R')
#         # -------------------------Text-----------------------------------------
#         pdf.ln(15)
#         pdf.set_font("TNR", 'B', size=10)
#         pdf.set_x(15)
#         pdf.multi_cell(180, 5, txt="Уважаемый {}".format(report.contract.customer.name), align='C')
#         # -------------------------Text-----------------------------------------
#         pdf.ln(15)
#         pdf.set_font("TNR", 'I', size=10)
#         pdf.set_x(15)
#         pdf.multi_cell(180, 5, txt="    В соответствии с Договором об оценке имущества № 25  от 1 Февраля 2020 года, оценщики ООО «AMIR AVTO BAHOLASH» провели оценку транспортного  средства марки {} Государственный номер {} зарегистрированного по адресу:{} Республика Узбекистан".format(report.car.brand,report.car.car_number,report.car.owner_address), align='J')
#         # -------------------------Create File-----------------------------------------
#         pdf.output("simple_dedmo.pdf")
#
#
#         return FileResponse(open("simple_dedmo.pdf", 'rb'))



class GeneratePDF(View):
    def get(self, request, id=id):
        locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")

        new_report_pdf = Report.objects.get(report_id=id)
        pdf = PyPDFML('example.xml')
        context = {
            'report': new_report_pdf,
            'services': new_report_pdf.service.all().__len__(),
            'datetime': str(new_report_pdf.created_at.strftime((" «%d»  %b  %Yг. ")))
        }
        pdf.generate(context)
        data = pdf.contents()

        filename = "%s.pdf" % new_report_pdf.car.car_number

        new_report_pdf.pdf_report.save(filename, ContentFile(data))

        return get_response(request, new_report_pdf.report_id)


def get_response(request, id):
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
