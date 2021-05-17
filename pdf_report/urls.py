from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('<int:id>/', GeneratePDF.as_view(), name='get_response'),
    path('mixing/<int:id>', GenerateMixing.as_view(), name='get_mixing'),
    path('agreement/<int:id>', GenerateAgreement.as_view(), name='get_agreement'),
    path('additional/<int:id>', GenerateAdditional.as_view(), name='get_additional'),
    path("download_xml/", get_base_template, name='download_xml'),
    path("make_pdf/", get_base, name='make_pdf'),
    path("download_xml_mixing/", get_base_mixing_template, name='download_xml_mixing'),
    path("download_xml_agreement/", get_base_agreement_template, name='download_xml_agreement'),
]
