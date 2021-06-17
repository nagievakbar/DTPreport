from django import forms
from .models import *
import datetime


class ReportForm(forms.ModelForm):
    """docstring for ReportForm."""

    report_date = forms.CharField(required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Дата отчёта', 'class': 'input_in'}))
    report_number = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={'placeholder': 'Номер отчёта', 'class': 'input_in'}))
    total_report_cost = forms.CharField(required=False,
                                        widget=forms.TextInput(attrs={'class': 'invisible_class all_sum'}))

    class Meta:
        model = Report
        fields = ['report_date', 'report_number', 'total_report_cost']


BRANDS = (
    ('Выберите Марку', "Выберите Марку"),
    ('Кобальт', 'Кобальт'),
    ('Спарк', 'Спарк'),
    ('Нексия3', 'Нексия3'),
    ('Малибу', 'Малибу'),
    ('Нексия Sonc', 'Нексия Sonc'),
    ('Дамас', 'Дамас'),
    ('Тико', 'Тико'),
    ('Тико', 'Тико'),
    ('Матиз', 'Матиз'),
    ('Матиз Бест', 'Матиз Бест'),
    ('Нексия Donc', 'Нексия Donc'),
    ('Ласетти', 'Ласетти'),
    ('Каптива', 'Каптива'),
    ('Такума', 'Такума'),
    ('Эпика', 'Эпика')
)

TYPE_CAR = (
    ('Выберите тип машины', 'Выберите тип машины'),
    ('Грузовой', 'Грузовой'),
    ('Легковой', 'Легковой')
)


class CarForm(forms.ModelForm):
    """docstring for CarForm."""
    brand_text = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'Марка', 'class': 'input_in'}))
    brand = forms.ChoiceField(choices=BRANDS, required=False,
                              widget=forms.Select(attrs={'class': 'form-control select-block drop-down-list'}))
    car_number = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'Номер машины', 'class': 'input_in'}))
    registration = forms.CharField(required=False,
                                   widget=forms.TextInput(attrs={'placeholder': 'Тех. паспорт', 'class': 'input_in'}))
    engine_number = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={'placeholder': 'Двигатель', 'class': 'input_in'}))
    body_number = forms.CharField(required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Кузов', 'class': 'input_in'}))
    chassis = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'Шасси', 'class': 'input_in'}))
    car_color = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'Цвет окраски', 'class': 'input_in'}))
    mileage = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'Пробег', 'class': 'input_in'}))
    release_date = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Год и месяц выпуска', 'class': 'input_in'}))

    car_owner = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'Владелец', 'class': 'input_in'}))
    owner_address = forms.CharField(required=False,
                                    widget=forms.Textarea(
                                        attrs={'placeholder': 'Адрес владельца', 'class': 'input_in',
                                               'onkeyup': 'textAreaAdjust(this)'}))
    type_of_car = forms.ChoiceField(
        required=False,
        choices=TYPE_CAR,
        widget=forms.Select(attrs={'class': 'form-control'}))

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
                  'car_owner',
                  'owner_address',
                  'type_of_car']


class ContractForm(forms.ModelForm):
    """docstring for ContractForm."""

    contract_date = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={'placeholder': 'Дата договора', 'class': 'input_in'}))
    contract_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Номер договора', 'class': 'input_in'}))

    class Meta:
        model = Contract
        fields = ['contract_date', 'contract_number']


class CalculationForm(forms.ModelForm):
    total = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'class': 'input2 work-price-input2 price_all total'}))
    departure = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'class': 'input2 work-price-input2 price_3 total'}))
    opr_ust = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'class': 'input2 work-price-input2 price_2 total'}))
    opr_damage = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={'class': 'input2 work-price-input2 price_1 total'}))

    class Meta:
        model = Calculation
        fields = [
            'total',
            'departure',
            'opr_ust',
            'opr_damage',
        ]


class ContractFormEdit(forms.ModelForm):
    """docstring for ContractForm."""
    contract_date = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Дата договора', 'class': 'input_in'}))
    contract_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Номер договора', 'class': 'input_in'}))

    class Meta:
        model = Contract
        fields = ['contract_date', 'contract_number']


class CustomerForm(forms.ModelForm):
    """docstring for CustomerForm."""

    name = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Заказчик', 'class': 'input_in'}))
    address = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'Адрес заказчика', 'class': 'input_in'}))
    passport_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Паспорт / Р/c № / в ', 'class': 'input_in'}))
    when_passport_issued = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Когда выдан / город', 'class': 'input_in'}))
    whom_passport_issued = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Кем выдан / МФО ОКЕД ИНН', 'class': 'input_in'}))
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Телефон', 'class': 'input_in'}))
    gnu_or_gje = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Г-ну', 'class': 'input_in'}))
    uvajaemaya = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'Уважаемый', 'class': 'input_in'}))

    mesto_osmotra = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Акт осмотра Место', 'class': 'input_in'}))

    class Meta:
        model = Customer
        fields = ['name', 'address', 'passport_number', 'when_passport_issued',
                  'whom_passport_issued', 'phone_number', 'gnu_or_gje', 'uvajaemaya', 'mesto_osmotra']


# class CustomerFormEdit(forms.ModelForm):
#     name = forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder': 'Заказчик', 'class': 'input_in'}))
#     address = forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder': 'Адрес заказчика', 'class': 'input_in'}))
#     passport_number = forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder': 'Паспорт', 'class': 'input_in'}))
#     when_passport_issued = forms.CharField(
#         required=False,
#         widget=forms.TextInput(attrs={'placeholder': 'Когда выдан', 'class': 'input_in'}))
#     whom_passport_issued = forms.CharField(
#         required=False,
#         widget=forms.TextInput(attrs={'placeholder': 'Кем выдан', 'class': 'input_in'}))
#     phone_number = forms.CharField(
#         required=False,widget=forms.TextInput(attrs={'placeholder': 'Телефон', 'class': 'input_in'}))
#
#     class Meta:
#         model = Customer
#         fields = ['name', 'address', 'passport_number', 'when_passport_issued',
#                   'whom_passport_issued', 'phone_number']


class ServiceForm(forms.Form):
    service_id = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input2 work-price-input2 first2'}))
    name = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'input2 work-price-input2 name2', 'onkeyup': 'textAreaAdjust(this)'}))
    norm_per_hour = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'input2 work-price-input2 time2'}))
    premium = forms.FloatField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input2 work-price-input2 allowance2'}))  # 'value': '0'
    price = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'input2 work-price-input2 price2'}))
    service_cost = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'input2 work-price-input2 sum2', 'readonly': ''}))
    # 'readonly': ''


# user = User.objects.get(id=u.__getitem__(0).myuser.user_id)
class ProductForm(forms.Form):
    name = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'input3 work-price-input3 name3', 'onkeyup': 'textAreaAdjust(this)'}))
    # unit = forms.CharField(
    # widget=forms.TextInput(attrs={'class': 'input3 work-price-input3 name3', 'readonly': ''}))
    quantity = forms.FloatField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input3 work-price-input3 time3', }))  # 'value': '0'
    price = forms.IntegerField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input3 work-price-input3 price3', }))
    product_cost = forms.IntegerField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input3 work-price-input3 sum3', 'readonly': ''}))


class ConsumableForm(forms.Form):
    consumable_id = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input4 work-price-input4 first4'}))
    name = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'input4 work-price-input4 name4', 'onkeyup': 'textAreaAdjust(this)'}))
    unit = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input4 work-price-input4 time4', }))
    quantity = forms.FloatField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input4 work-price-input4 allowance4', }))  # 'value': '0'
    price = forms.IntegerField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input4 work-price-input4 price4', }))
    consumable_cost = forms.IntegerField(
        required=False,
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
        required=False,
        widget=forms.TextInput(attrs={'class': 'input work-price-input point-input'}))
    weight = forms.IntegerField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input work-price-input weight-input'}))
    wear = forms.IntegerField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input work-price-input prehnite-input', 'readonly': ""}))
    accept_wear = forms.IntegerField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input work-price-input prehnite-input'}))
