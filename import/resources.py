from import_export import resources
from makereport.models import Product, Service, Consumable


class ProductResources(resources.ModelResource):
    class Meta:
        model = Product
        exclude = ('id',)
        import_id_fields = ('product_id',)
        force_init_instance = False


class ServiceResources(resources.ModelResource):

    class Meta:
        model = Service
        exclude = ('id',)
        import_id_fields = ('service_id',)
        force_init_instance = False


class ConsumableResources(resources.ModelResource):
    class Meta:
        model = Consumable
        exclude = ('id',)
        import_id_fields = ('consumable_id',)
        force_init_instance = False
