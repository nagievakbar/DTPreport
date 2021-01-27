from django import forms
from .models import *
import datetime


class ReportForm(forms.ModelForm):
    """docstring for ReportForm."""

    created_at = forms.DateField(input_formats=['%d.%m.%Y'], widget=forms.DateInput(attrs={'value': datetime.date.today().strftime("%d.%m.%Y") , 'class': 'input'}))
    # media_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'file-input', 'id': 'chooseFile'}))

    class Meta:
        model = Report
        fields = ['created_at']

        # 'media_photo']
        # 'created_at',


class CarForm(forms.ModelForm):
    """docstring for CarForm."""

    brand = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Марка', 'class': 'input'}))
    car_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Номер машины', 'class': 'input'}))
    registration = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Тех. паспорт', 'class': 'input'}))
    engine_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Двигатель', 'class': 'input'}))
    body_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Кузов', 'class': 'input'}))
    chassis = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Шасси', 'class': 'input'}))
    car_color = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Цвет окраски', 'class': 'input'}))
    mileage = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Пробег', 'class': 'input'}))
    release_date = forms.DateField(input_formats=['%Y'], widget=forms.DateInput(attrs={'placeholder': 'Год и месяц выпуска', 'class': 'input'}))
    car_type = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Тип', 'class': 'input'}))
    car_owner = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Владелец', 'class': 'input'}))
    owner_address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Адрес владельца', 'class': 'input'}))

    class Meta:
        model = Car
        fields = ['brand',
                  'car_number',
                  'registration',
                  'engine_number',
                  'body_number',
                  'chassis',
                  'car_color',
                  'mileage',
                  'release_date',
                  'car_type',
                  'car_owner',
                  'owner_address']


class ContractForm(forms.ModelForm):
    """docstring for ContractForm."""

    class Meta:
        model = Contract
        fields = ['customer']


class CustomerForm(forms.ModelForm):
    """docstring for CustomerForm."""

    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Заказчик', 'class': 'input'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Адрес заказчика', 'class': 'input'}))
    passport_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Паспорт', 'class': 'input'}))
    when_passport_issued = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Когда выдан', 'class': 'input'}))
    whom_passport_issued = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Кем выдан', 'class': 'input'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Телефон', 'class': 'input'}))


    class Meta:
        model = Customer
        fields = ['name', 'address', 'passport_number', 'when_passport_issued',
                  'whom_passport_issued', 'phone_number']


class ServiceForm(forms.Form):

    service_id = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'ID', 'class': 'input input-service_id'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Название', 'class': 'input input-name', 'readonly': ''}))
    norm_per_hour= forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'нор\час', 'class': 'input input-nph', 'readonly': ''}))
    premium = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'надбавка', 'class': 'input input-premium', 'value': '0'}))
    price = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'цена', 'class': 'input input-price', 'readonly': ''}))
    service_cost = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'сумма', 'class': 'input input-cost', 'readonly': ''}))
    # 'readonly': ''

# user = User.objects.get(id=u.__getitem__(0).myuser.user_id)
class ProductForm(forms.Form):

    product_id = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'ID', 'class': 'input input-product_id'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Название', 'class': 'input input-name', 'readonly': ''}))
    unit = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ед.изм', 'class': 'input input-unit', 'readonly': ''}))
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'надбавка', 'class': 'input input-quantity','value': '0'}))
    price = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'цена', 'class': 'input input-price', 'readonly': ''}))
    product_cost = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'сумма', 'class': 'input input-cost', 'readonly': ''}))


class ConsumableForm(forms.Form):

    consumable_id = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'ID', 'class': 'input input-consumable_id'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Название', 'class': 'input input-name', 'readonly': ''}))
    unit = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ед.изм', 'class': 'input input-unit', 'readonly': ''}))
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'надбавка', 'class': 'input input-quantity-cons','value': '0'}))
    price = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'цена', 'class': 'input input-price', 'readonly': ''}))
    consumable_cost = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'сумма', 'class': 'input input-cost', 'readonly': ''}))


class WearForm(forms.Form):

    point = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Баллы', 'class': 'input work-price-input point-input'}))
    weight = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Т', 'class': 'input work-price-input weight-input'}))
    wear = forms.IntegerField(widget=forms.TextInput(attrs={'class':'input work-price-input wear-input'}))
    accept_wear = forms.IntegerField(widget=forms.TextInput(attrs={'class':'input work-price-input accept-wear-input'}))


class ReportRateSettingForm(forms.ModelForm):

    report_rate_price = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'input-rate-price'}))

    class Meta:
        model = MyUser
        fields = ['report_rate_price']

