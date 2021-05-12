from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from .converters import num2text
import random
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class Contract(models.Model):
    contract_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    customer = models.ForeignKey('Customer', null=True, blank=True, on_delete=models.CASCADE, related_name='Customer',
                                 verbose_name='Клиент')
    pdf_contract = models.FileField(blank=True, null=True, verbose_name='Контракт в пдф')
    contract_date = models.CharField(max_length=10, null=True, blank=True)
    contract_number = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.contract_id)

    class Meta:
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'


BRANDS = (
    ('Выберите Марку', 'Выберите Марку'),
    ('Кобальт', 'Кобальт'),
    ('Спарк', 'Спарк'),
    ('Нексия3', 'Нексия3'),
    ('Малибу', 'Малибу'),
    ('Нексия Sonc', 'Нексия Sonc'),
    ('Дамас', 'Дамас'),
    ('Тико', 'Тико'),
    ('Матиз', 'Матиз'),
    ('Матиз Бест', 'Матиз Бест'),
    ('Нексия Donc', 'Нексия Donc'),
    ('Ласетти', 'Ласетти'),
    ('Каптива', 'Каптива'),
    ('Такума', 'Такума'),
    ('Эпика', 'Эпика')
)


class Car(models.Model):
    car_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    brand_text = models.CharField(max_length=30)
    brand = models.CharField(max_length=30, choices=BRANDS, null=True, blank=True)
    car_number = models.CharField(max_length=8)
    registration = models.CharField(max_length=15)
    engine_number = models.CharField(max_length=30)
    body_number = models.CharField(max_length=30)
    chassis = models.CharField(max_length=30)
    car_color = models.CharField(max_length=20)
    mileage = models.CharField(max_length=10)
    release_date = models.DateField()
    car_type = models.CharField(max_length=20)
    car_owner = models.CharField(max_length=60)
    owner_address = models.CharField(max_length=100)
    type_of_car = models.CharField(max_length=50, choices=(('Грузовой', 'Грузовой'), ('Легковой', 'Легковой')))

    def __str__(self):
        return str(self.car_number) + ' ' + str(self.brand)

    class Meta:
        verbose_name = 'Машину'
        verbose_name_plural = 'Машины'


class Documents(models.Model):
    license = models.ImageField(blank=True, null=True, verbose_name='Лицензия')
    guvonhnoma = models.ImageField(blank=True, null=True, verbose_name='Гувохнома')
    certificate = models.ImageField(blank=True, null=True, verbose_name='Сертификат')
    insurance = models.ImageField(blank=True, null=True, verbose_name='Cтраховка')

    class Meta:
        verbose_name = 'Фотографии для документа'
        verbose_name_plural = 'Фотографии для документов'

    def __str__(self):
        return "Документ № {}".format(self.id)


class Customer(models.Model):
    customer_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100, verbose_name='ФИО')
    address = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=9, verbose_name='Паспорт')
    when_passport_issued = models.DateField()
    whom_passport_issued = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, verbose_name='Тел. номер')
    gnu_or_gje = models.CharField(max_length=40)
    uvajaemaya = models.CharField(max_length=40)
    mesto_osmotra = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Клиента'
        verbose_name_plural = 'Клиенты'


class Product(models.Model):
    product_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100, )
    unit = models.CharField(max_length=10, verbose_name='Ед.измер.')
    nexia3 = models.FloatField(blank=True, null=True, verbose_name='Нексия 3')
    cobalt = models.FloatField(blank=True, null=True, verbose_name='Кобальт')
    malibu = models.FloatField(blank=True, null=True, verbose_name='Малибу')
    nexia_sonc = models.FloatField(blank=True, null=True, verbose_name='Нексия Sonc')
    damas = models.FloatField(blank=True, null=True, verbose_name='Дамас')
    tiko = models.FloatField(blank=True, null=True, verbose_name='Тико')
    matiz = models.FloatField(blank=True, null=True, verbose_name='Матиз')
    matiz_best = models.FloatField(blank=True, null=True, verbose_name='Матиз Бест')
    spark = models.FloatField(blank=True, null=True, verbose_name='Спарк')
    nexia_dons = models.FloatField(blank=True, null=True, verbose_name='Нексия Донс')
    lacceti = models.FloatField(blank=True, null=True, verbose_name='Лассети')
    captiva = models.FloatField(blank=True, null=True, verbose_name='Каптива')
    takuma = models.FloatField(blank=True, null=True, verbose_name='Такума')
    epica = models.FloatField(blank=True, null=True, verbose_name='Эпика')

    price = models.IntegerField(blank=True, null=True, verbose_name='Цена')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Деталь'
        verbose_name_plural = 'Детали'


class Service(models.Model):
    service_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')
    name = models.CharField(max_length=1000, blank=True, null=True)
    nexia3 = models.FloatField(blank=True, null=True, verbose_name='Нексия 3')
    cobalt = models.FloatField(blank=True, null=True, verbose_name='Кобальт')
    malibu = models.FloatField(blank=True, null=True, verbose_name='Малибу')
    nexia_sonc = models.FloatField(blank=True, null=True, verbose_name='Нексия Sonc')
    damas = models.FloatField(blank=True, null=True, verbose_name='Дамас')
    tiko = models.FloatField(blank=True, null=True, verbose_name='Тико')
    matiz = models.FloatField(blank=True, null=True, verbose_name='Матиз')
    matiz_best = models.FloatField(blank=True, null=True, verbose_name='Матиз Бест')
    spark = models.FloatField(blank=True, null=True, verbose_name='Спарк')
    nexia_dons = models.FloatField(blank=True, null=True, verbose_name='Нексия Донс')
    lacceti = models.FloatField(blank=True, null=True, verbose_name='Лассети')
    captiva = models.FloatField(blank=True, null=True, verbose_name='Каптива')
    takuma = models.FloatField(blank=True, null=True, verbose_name='Такума')
    epica = models.FloatField(blank=True, null=True, verbose_name='Эпика')

    price = models.IntegerField(blank=True, null=True, verbose_name='Цена')

    BRANDS = {
        'Кобальт': cobalt,
        'Спарк': spark,
        'Нексия3': nexia3,
        'Малибу': malibu,
        'Нексия Sonc': nexia_sonc,
        'Дамас': damas,
        'Тико': tiko,
        'Матиз': matiz,
        'Матиз Бест': matiz_best,
        'Нексия Donc': nexia_dons,
        'Ласетти': lacceti,
        'Каптива': captiva,
        'Такума': takuma,
        'Эпика': epica
    }

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Услугу'
        verbose_name_plural = 'Услуги'


class Consumable(models.Model):
    consumable_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=10, verbose_name='Ед.измер.')

    price = models.IntegerField(blank=True, null=True, verbose_name='Цена')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Расходник'
        verbose_name_plural = 'Расходники'


def handler_base(instance, filename):
    return "templates_xml/base.xml"


def handler_base_mixing(instance, filename):
    return "templates_xml/mixing.xml"


def handler_base_agreement(instance, filename):
    return "templates_xml/agreement.xml"


def handler_base_additional(instance, filename):
    return "templates_xml/additional.xml"


class TemplateBase(models.Model):
    template = models.FileField(blank=True, null=True, upload_to=handler_base,
                                verbose_name='Шаблон для отчета')

    def delete(self, *args, **kwargs):
        default_storage.delete(self.template.path)
        super(TemplateBase, self).delete(*args, **kwargs)


class TemplateMixing(models.Model):
    template = models.FileField(blank=True, null=True, upload_to=handler_base_mixing,
                                verbose_name='Шаблоны для заключения')

    def delete(self, *args, **kwargs):
        default_storage.delete(self.template.path)
        super(TemplateMixing, self).delete(*args, **kwargs)


class TemplateAdditional(models.Model):
    template = models.FileField(blank=True, null=True, upload_to=handler_base_additional,
                                verbose_name='Шаблоны для дополнения')

    def delete(self, *args, **kwargs):
        default_storage.delete(self.template.path)
        super(TemplateAdditional, self).delete(*args, **kwargs)


class TemplateAgreement(models.Model):
    template = models.FileField(blank=True, null=True, upload_to=handler_base_agreement,
                                verbose_name='Шаблоны для догвора')

    def delete(self, *args, **kwargs):
        default_storage.delete(self.template.path)
        super(TemplateAgreement, self).delete(*args, **kwargs)


class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    report_rate_price = models.IntegerField(default=0, blank=True, null=True)
    report_rate_price_txt = models.CharField(max_length=200, blank=True, null=True)

    @receiver(post_save, sender=User)
    def update_profile_signal(sender, instance, created, **kwargs):
        if created:
            MyUser.objects.create(user=instance)
        instance.myuser.save()




class HoldsImages(models.Model):
    image = models.ManyToManyField('Images')
    image_previous = models.ManyToManyField('Images', related_name="image_previous")
    pp_photo = models.ManyToManyField('PassportPhotos')
    pp_photo_previous = models.ManyToManyField('PassportPhotos', related_name="pp_photo_previous")
    o_images = models.ManyToManyField('OtherPhotos')
    o_images_previous = models.ManyToManyField('OtherPhotos', related_name="o_photo_previous")
    checks = models.ManyToManyField('Checks')
    checks_previous = models.ManyToManyField('Checks', related_name="check_previous")
    report = models.ForeignKey('Report', blank=True, null=True, on_delete=models.CASCADE)

    def create_new(self, old):
        self.image.set(old.image.all())
        self.pp_photo.set(old.pp_photo.all())
        self.o_images.set(old.o_images.all())
        self.checks.set(old.checks.all())
        self.save()

    def set_new(self, old):
        self._clear()
        self.image_previous.set(old.image.all())
        self.pp_photo_previous.set(old.pp_photo.all())
        self.o_images_previous.set(old.o_images.all())
        self.checks_previous.set(old.checks.all())
        self.save()

    def store_add(self):
        self._store(self.image_previous.all(), self.image)
        self._store(self.pp_photo_previous.all(), self.pp_photo)
        self._store(self.o_images_previous.all(), self.o_images)
        self._store(self.checks_previous.all(), self.checks)
        self.save()

    def _clear(self):
        self.image_previous.clear()
        self.pp_photo_previous.clear()
        self.o_images_previous.clear()
        self.checks_previous.clear()

    def image_concatinate(self):
        return list(self.image_previous.all()) + list(self.image.all())

    def pp_photo_concatinate(self):
        return list(self.pp_photo_previous.all()) + list(self.pp_photo.all())

    def check_concatinate(self):
        return list(self.checks_previous.all()) + list(self.checks.all())

    def o_photo_concatinate(self):
        return list(self.o_images.all()) + list(self.o_images_previous.all())

    def _store(self, from_model, to_model):
        for each in from_model:
            to_model.add(each)


class Images(models.Model):
    image_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    image = models.ImageField(blank=True, null=True, verbose_name='Фото')
    report = models.ForeignKey('Report', on_delete=models.CASCADE, blank=True, null=True, related_name='reportImages',
                               verbose_name='Отчёт')

    def delete(self, *args, **kwargs):
        default_storage.delete(self.image.path)
        super(Images, self).delete(*args, **kwargs)


class PassportPhotos(models.Model):
    p_photo_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    photo = models.ImageField(blank=True, null=True, verbose_name='Фото пасспорта')
    report = models.ForeignKey('Report', on_delete=models.CASCADE, blank=True, null=True, related_name='reportPPhotos',
                               verbose_name='Отчёт')

    def delete(self, *args, **kwargs):
        default_storage.delete(self.photo.path)
        super(PassportPhotos, self).delete(*args, **kwargs)


class OtherPhotos(models.Model):
    o_photo_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    photos = models.ImageField(blank=True, null=True, verbose_name='Фото чеков')
    report = models.ForeignKey('Report', on_delete=models.CASCADE, blank=True, null=True, related_name='reportOPhotos',
                               verbose_name='Отчёт')

    def delete(self, *args, **kwargs):
        default_storage.delete(self.photos.path)
        super(OtherPhotos, self).delete(*args, **kwargs)


class CustomSum(models.Model):
    sum = models.IntegerField(default=0, verbose_name="Введите сумму")

    class Meta:
        verbose_name = 'Сумма'
        verbose_name_plural = 'Сумма'

    def __str__(self):
        return str(self.sum)


class Checks(models.Model):
    checks_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    checks = models.ImageField(blank=True, null=True, verbose_name='Фото чеков')
    report = models.ForeignKey('Report', on_delete=models.CASCADE, blank=True, null=True, related_name='reportChecks',
                               verbose_name='Отчёт')

    def delete(self, *args, **kwargs):
        default_storage.delete(self.checks.path)
        super(Checks, self).delete(*args, **kwargs)


class Report(models.Model):
    report_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    report_number = models.CharField(max_length=10)
    report_date = models.CharField(max_length=10)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by', verbose_name='Создан')
    created_at = models.DateField(blank=True, null=True, verbose_name='Время создания')

    car = models.ForeignKey('Car', on_delete=models.CASCADE, related_name='Car', verbose_name='Машина')
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE, related_name='Contract', verbose_name='Контракт')

    service = models.ManyToManyField(Service, related_name='Услуги', verbose_name='Услуги')
    product = models.ManyToManyField(Product, related_name='Детали', verbose_name='Детали')
    consumable = models.ManyToManyField(Consumable, related_name='Расходники', verbose_name='Расходники')

    service_cost = models.IntegerField(default=0)
    product_cost = models.IntegerField(default=0)
    product_acc_cost = models.IntegerField(default=0)
    consumable_cost = models.IntegerField(default=0)
    key = models.CharField(max_length=13, blank=True)

    total_report_cost = models.CharField(max_length=15)
    total_report_cost_txt = models.CharField(max_length=200)

    pdf_report = models.FileField(blank=True, null=True, upload_to='uploads/%Y/%m/%d/', verbose_name='Отчёт в пдф')
    pdf_report_base64 = models.CharField(max_length=1000000, blank=True, null=True)
    pdf_report_pkcs7 = models.JSONField(blank=True, null=True)
    pdf_report_qr = models.JSONField(blank=True, null=True)
    pdf_qr_code_user = models.CharField(max_length=500, blank=True, null=True)
    pdf_qr_code_company = models.CharField(max_length=500, blank=True, null=True)
    signed = models.BooleanField(default=False)
    signed_by_boss = models.BooleanField(default=False)

    passport_photo = models.FileField(blank=True, null=True, verbose_name='Фото пасспорта')
    registration_photo = models.FileField(blank=True, null=True, verbose_name='Фото тех.пасспорта')

    wear_data = models.JSONField(blank=True, null=True)
    service_data = models.JSONField(blank=True, null=True)
    product_data = models.JSONField(blank=True, null=True)
    consumable_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return str(self.report_id)

    def delete(self, *args, **kwargs):
        try:
            default_storage.delete(self.passport_photo.path)
            default_storage.delete(self.registration_photo.path)
            default_storage.delete(self.pdf_report)
        except ValueError:
            pass
        finally:
            self.car.delete()
            self.contract.customer.delete()
            self.contract.delete()
        return super(Report, self).delete(*args, **kwargs)

    def get_product_acc_cost(self):
        print('get_product_acc_cost')
        self.product_acc_cost = (self.product_cost * (1 - self.wear_data.__getitem__('accept_wear') / 100))
        return self.product_acc_cost

    def get_total_report_price(self):
        print('get_total_report_price')
        self.total_report_cost = ' '.join(
            '{:,}'.format(int(self.service_cost + self.get_product_acc_cost() + self.consumable_cost)).split(','))

    def get_total_report_cost_txt(self):
        self.total_report_cost_txt = num2text(
            int(self.service_cost + self.get_product_acc_cost() + self.consumable_cost),
            main_units=((u'сум', u'сумы', u'суммов'), 'f'))
        return self.total_report_cost_txt

    def set_private_key(self):
        while True:
            figure = uuid.uuid4().hex[:12].upper()
            if not Report.objects.filter(key=figure).exists():
                break
        self.key = figure


    class Meta:
        verbose_name = 'Отчёт'
        verbose_name_plural = 'Отчёты'


class Calculation(models.Model):
    total = models.CharField(max_length=20)
    departure = models.CharField(max_length=20)
    opr_ust = models.CharField(max_length=20)
    opr_damage = models.CharField(max_length=20)
    report = models.ForeignKey('Report', on_delete=models.CASCADE, related_name='report', verbose_name='Репорт',
                               null=True, blank=True)

    def get_total_report_cost_txt(self):
        report_rate_price_txt = num2text(int(self.total.strip().replace(' ', "")), main_units=((u'сум', u'сумы', u'сум'), 'f'))
        return report_rate_price_txt
