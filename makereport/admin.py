from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import *


# Register your models here.
admin.site.register(Customer)
admin.site.register(Contract)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_id',
                    'car',
                    'created_at',
                    'created_by',
                    'contract',
                    'pdf_report'
    )
    search_fields = ['report_id']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('car_id',
                    'car_number',

    )
    search_fields = ['car_id']


