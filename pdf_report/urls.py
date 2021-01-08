from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('<int:id>/', GeneratePDF.as_view(), name='pdf_report'),
    path('<int:id>/', get_response, name='get_response')
]
