from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('<int:id>/', GeneratePDF.as_view(), name='get_response'),
    path("download_xml/", get_base_template, name='download_xml')
]
