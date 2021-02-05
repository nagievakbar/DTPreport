from django.urls import path
# from DTPreport.urls import admin
from django.contrib import admin
from .views import *
from .utils import *


urlpatterns = [
    path('list', reports_list, name='reports_list'),
    path('create/', ReportView.as_view(), name='new_report'),
    path('<str:extend>/<int:id>', ReportView.as_view(), name='extend_report'),
    path('<int:id>/edit/', ReportView.as_view(), name='edit_report'),
    path('<int:id>/delete/', ReportView.as_view(), name='delete_report'),
    path('user_settings/', UserSettingsView.as_view(), name='user_settings'),
    path('sign/', get_sign, name='get_sight'),
    path('input/', test_input, name='test_input'),
    path(r'ajax/get_service_ajax/', get_service_ajax, name='get_service_ajax'),
    path(r'ajax/get_service_cost/', get_service_cost, name='get_service_cost'),
    path(r'ajax/get_product_ajax/', get_product_ajax, name='get_product_ajax'),
    path(r'ajax/get_product_cost/', get_product_cost, name='get_product_cost'),
    path(r'ajax/get_consumable_cost/', get_consumable_cost, name='get_consumable_cost'),
    path(r'ajax/get_consumable_ajax/', get_consumable_ajax, name='get_consumable_ajax'),
    path(r'ajax/get_wear_ajax/', get_wear_ajax, name='get_wear_ajax'),
    path(r'ajax/get_car_card/', get_car_card, name='get_car_card'),
    path(r'ajax/get_btn_to_download/', get_btn_to_download, name='get_btn_to_download'),

]