from django import forms
from .models import *
import datetime
class ReportForm(forms.ModelForm):
    """docstring for ReportForm."""

    report_date = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Дата отчёта', 'class': 'input_in'}))
    report_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Номер отчёта', 'class': 'input_in'}))

    class Meta:
        model = Report
        fields = ['report_date', 'report_number']

BRANDS = (
        (0, "Выберите Марку"),
        ('Кобальт', 'Кобальт'),
        ('Спарк', 'Спарк'),
        ('Нексия3', 'Нексия3'),
        ('Малибу','Малибу'),
        ('Нексия Sonc', 'Нексия Sonc'),
        ('Дамас', 'Дамас'),
        ('Тико','Тико'),
        ('Матиз', 'Матиз'),
        ('Матиз Бест', 'Матиз Бест'),
        ('Нексия Donc', 'Нексия Donc'),
        ('Ласетти','Ласетти'),
        ('Каптива',  'Каптива'),
        ('Такума',  'Такума'),
        ('Эпика',  'Эпика')
    )
class CarForm(forms.ModelForm):
    """docstring for CarForm."""
    brand_text = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Марка', 'class': 'input_in'}))
    brand = forms.ChoiceField(choices=BRANDS, widget=forms.Select(attrs={'class':'form-control select-block'}))
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
        fields = ['brand_text',
                  'brand',
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

    contract_date = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Дата договора', 'class': 'input_in'}))
    contract_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Номер договора', 'class': 'input_in'}))

    class Meta:
        model = Contract
        fields = ['contract_date', 'contract_number']


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
    gnu_or_gje = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Г-ну', 'class': 'input_in'}))
    uvajaemaya = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Уважаемый', 'class': 'input_in'}))
    vid = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Вид', 'class': 'input_in'}))
    mesto_osmotra = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Акт осмотра Место', 'class': 'input_in'}))

    class Meta:
        model = Customer
        fields = ['name', 'address', 'passport_number', 'when_passport_issued',
                  'whom_passport_issued', 'phone_number', 'gnu_or_gje', 'uvajaemaya', 'vid', 'mesto_osmotra']


class ServiceForm(forms.Form):
    service_id = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'input2 work-price-input2 first2'}))
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input2 work-price-input2 name2'}))
    norm_per_hour = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'input2 work-price-input2 time2'}))
    premium = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input2 work-price-input2 allowance2' }))  # 'value': '0'
    price = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'input2 work-price-input2 price2'}))
    service_cost = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'input2 work-price-input2 sum2', 'readonly': ''}))
    # 'readonly': ''


# user = User.objects.get(id=u.__getitem__(0).myuser.user_id)
class ProductForm(forms.Form):
    product_id = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'input3 work-price-input3 count'}))
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input3 work-price-input3 name3', }))
    # unit = forms.CharField(
        # widget=forms.TextInput(attrs={'class': 'input3 work-price-input3 name3', 'readonly': ''}))
    quantity = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'input3 work-price-input3 time3', }))  # 'value': '0'
    price = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'input3 work-price-input3 price3', }))
    product_cost = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'input3 work-price-input3 sum3', 'readonly': ''}))


class ConsumableForm(forms.Form):
    consumable_id = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'input4 work-price-input4 first4'}))
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input4 work-price-input4 name4', }))
    unit = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input4 work-price-input4 time4', }))
    quantity = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'input4 work-price-input4 allowance4', }))  # 'value': '0'
    price = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'input4 work-price-input4 price4', }))
    consumable_cost = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'input4 work-price-input4 sum4', 'readonly': ''}))


class ImageForm(forms.ModelForm):
    image = forms.CharField(
        required=False,
        widget=forms.FileInput(
            attrs={'id': 'imageinput', 'type': 'file', 'name': 'input', 'multiple': True, 'required': False}))

    class Meta:
        model = Images
        fields = ['image']


class PPhotoForm(forms.ModelForm):
    photo = forms.CharField(
        required=False,
        widget=forms.FileInput(
            attrs={'id': 'pphotoinput', 'type': 'file', 'name': 'input', 'multiple': True}))

    class Meta:
        model = PassportPhotos
        fields = ['photo']


class OPhotoForm(forms.ModelForm):
    photos = forms.CharField(
        required=False,
        widget=forms.FileInput(
            attrs={'id': 'ophotoinput', 'type': 'file', 'name': 'input', 'multiple': True}))

    class Meta:
        model = OtherPhotos
        fields = ['photos']


class ChecksForm(forms.ModelForm):
    checks = forms.CharField(
        required=False,
        widget=forms.FileInput(
            attrs={'id': 'checksinput', 'type': 'file', 'name': 'input', 'multiple': True}))

    class Meta:
        model = Checks
        fields = ['checks']


class WearForm(forms.Form):
    point = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'input work-price-input point-input'}))
    weight = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'input work-price-input weight-input'}))
    wear = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'input work-price-input prehnite-input'}))
    accept_wear = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'input work-price-input prehnite-input'}))

class TemplateForm(forms.Form):
    template = forms.CharField(
        widget=forms.FileInput(
            attrs={'id': 'pphotoinput', 'type': 'file', 'name': 'input', 'multiple': True}))

    class Meta:
        model = MyUser
        fields = ['template']