from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    # path('<int:id>/', , name='pdf_report'),
    path('<int:id>/', GeneratePDF.as_view(), name='get_response')
]
