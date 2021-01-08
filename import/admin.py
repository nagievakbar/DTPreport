from django.contrib import admin
from makereport.models import Product, Service, Consumable
from import_export.admin import ImportExportModelAdmin


class ProductAdmin(ImportExportModelAdmin):
    list_display = ('product_id', 'unit',
                    'price',
                    'nexia3',
                    'cobalt',
                    'malibu',
                    'nexia_sonc',
                    'damas',
                    'tiko',
                    'matiz',
                    'matiz_best',
                    'spark',
                    'nexia_dons',
                    'lacceti',
                    'captiva',
                    'takuma',
                    'epica'
                    )
    search_fields = ['product_id']


class ServiceAdmin(ImportExportModelAdmin):
    list_display = ('service_id',
                    'price',
                    'nexia3',
                    'cobalt',
                    'malibu',
                    'nexia_sonc',
                    'damas',
                    'tiko',
                    'matiz',
                    'matiz_best',
                    'spark',
                    'nexia_dons',
                    'lacceti',
                    'captiva',
                    'takuma',
                    'epica'
                    )
    search_fields = ['service_id']


class ConsumableAdmin(ImportExportModelAdmin):
    list_display = ('consumable_id', 'name', 'unit',
                    'price',
                    )
    search_fields = ['consumable_id']


admin.site.register(Consumable, ConsumableAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Product, ProductAdmin)
