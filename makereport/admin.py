from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from makereport.models import MyUser
from .models import *


class MyUserInline(admin.StackedInline):
    model = MyUser
    can_delete = False
    verbose_name_plural = 'Мои Пользователи'


class UserAdmin(BaseUserAdmin):
    inlines = (MyUserInline,)
# Register your models here.


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_id',
                    'car',
                    'created_at',
                    'created_by',
                    'contract',
                    'pdf_report',
                    'wear_data',
                    'product_data',
                    'service_data',
                    'consumable_data'
    )
    search_fields = ['report_id']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('car_id',
                    'brand',
                    'car_number',
                    'car_owner'
    )
    search_fields = ['car_number',
                     'brand']


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

