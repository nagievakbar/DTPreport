from django import forms
from .models import *
import datetime


class ReportForm(forms.ModelForm):
    """docstring for ReportForm."""

    created_at = forms.DateField(input_formats=['%d.%m.%Y'], widget=forms.DateInput(
        attrs={'value': datetime.date.today().strftime("%d.%m.%Y"), 'class': 'input_in'}))

    # media_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'file-input', 'id': 'chooseFile'}))

    class Meta:
        model = Report
        fields = ['created_at']

        # 'media_photo']
        # 'created_at',


class CarForm(forms.ModelForm):
    """docstring for CarForm."""

    brand = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Марка', 'class': 'input_in'}))
    car_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Номер машины', 'class': 'input_in'}))
    registration = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Тех. паспорт', 'class': 'input_in'}))
    engine_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Двигатель', 'class': 'input_in'}))
    body_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Кузов', 'class': 'input_in'}))
    chassis = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Шасси', 'class': 'input_in'}))
    car_color = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Цвет окраски', 'class': 'input_in'}))
    mileage = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Пробег', 'class': 'input_in'}))
    release_date = forms.DateField(input_formats=['%Y'], widget=forms.DateInput(
        attrs={'placeholder': 'Год и месяц выпуска', 'class': 'input_in'}))
    car_type = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Тип', 'class': 'input_in'}))
    car_owner = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Владелец', 'class': 'input_in'}))
    owner_address = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Адрес владельца', 'class': 'input_in'}))

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

    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Заказчик', 'class': 'input_in'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Адрес заказчика', 'class': 'input_in'}))
    passport_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Паспорт', 'class': 'input_in'}))
    when_passport_issued = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Когда выдан', 'class': 'input_in'}))
    whom_passport_issued = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Кем выдан', 'class': 'input_in'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Телефон', 'class': 'input_in'}))

    class Meta:
        model = Customer
        fields = ['name', 'address', 'passport_number', 'when_passport_issued',
                  'whom_passport_issued', 'phone_number']


class ServiceForm(forms.Form):
    service_id = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'input2 work-price-input2 first2'}))
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input2 work-price-input2 name2', 'readonly': ''}))
    norm_per_hour = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'input2 work-price-input2 time2', 'readonly': ''}))
    premium = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input2 work-price-input2 allowance2', })) #'value': '0'
    price = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'input2 work-price-input2 price2', 'readonly': ''}))
    service_cost = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'input2 work-price-input2 sum2', 'readonly': ''}))
    # 'readonly': ''


# user = User.objects.get(id=u.__getitem__(0).myuser.user_id)
class ProductForm(forms.Form):
    product_id = forms.IntegerField(
        widget=forms.TextInput(attrs={ 'class': 'input3 work-price-input3 count'}))
    name = forms.CharField(
        widget=forms.TextInput(attrs={ 'class': 'input3 work-price-input3 name3', 'readonly': ''}))
    unit = forms.CharField(
        widget=forms.TextInput(attrs={ 'class': 'input3 work-price-input3 name3', 'readonly': ''}))
    quantity = forms.IntegerField(
        widget=forms.TextInput(attrs={ 'class': 'input3 work-price-input3 time3', })) #'value': '0'
    price = forms.IntegerField(
        widget=forms.TextInput(attrs={ 'class': 'input3 work-price-input3 price3', 'readonly': ''}))
    product_cost = forms.IntegerField(
        widget=forms.TextInput(attrs={ 'class': 'input3 work-price-input3 sum3', 'readonly': ''}))


class ConsumableForm(forms.Form):
    consumable_id = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'input4 work-price-input4 first4'}))
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input4 work-price-input4 name4', 'readonly': ''}))
    unit = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input4 work-price-input4 time4', 'readonly': ''}))
    quantity = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'input4 work-price-input4 allowance4', })) #'value': '0'
    price = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'input4 work-price-input4 price4', 'readonly': ''}))
    consumable_cost = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'input4 work-price-input4 sum4', 'readonly': ''}))


class ImageForm(forms.ModelForm):
    image = forms.CharField(
        widget=forms.FileInput(attrs={'id': 'kv-explorer', 'name': 'input', 'required': False, 'multiple': True}))

    class Meta:
        model = Images
        fields = ['image']


class WearForm(forms.Form):
    point = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'input work-price-input point-input'}))
    weight = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'input work-price-input weight-input'}))
    wear = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'input work-price-input prehnite-input'}))
    accept_wear = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'input work-price-input prehnite-input'}))


class ReportRateSettingForm(forms.ModelForm):
    report_rate_price = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'input-rate-price'}))

    class Meta:
        model = MyUser
        fields = ['report_rate_price']
