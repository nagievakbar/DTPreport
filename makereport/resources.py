from import_export import resources
from .models import *


class ServicesAdmin(resources.ModelResource):
    class Meta:
        model = Service
        exclude = ('id',)
