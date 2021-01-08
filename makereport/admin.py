from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import *


# Register your models here.

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

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id',
                    'name',
                    'phone_number',
                    'passport_number',
    )
    search_fields = ['passport_number']

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('contract_id',
                    'customer',
    )
    search_fields = ['customer']

