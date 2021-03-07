from django.db import models
from django.contrib.auth.models import User
from .converters import num2text


class Contract(models.Model):
    contract_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='Customer', verbose_name='Клиент')
    pdf_contract = models.FileField(blank=True, null=True, verbose_name='Контракт в пдф')
    contract_date = models.CharField(max_length=10, null=True, blank=True)
    contract_number = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.contract_id)

    class Meta:
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'


class Car(models.Model):
    car_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    brand = models.CharField(max_length=30)
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

    def __str__(self):
        return str(self.car_number) + ' ' + str(self.brand)

    class Meta:
        verbose_name = 'Машину'
        verbose_name_plural = 'Машины'


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
    vid = models.CharField(max_length=100)
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
    service_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
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


class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    report_rate_price = models.IntegerField(default=0, blank=True, null=True)
    report_rate_price_txt = models.CharField(max_length=200, blank=True, null=True)

    def get_total_report_cost_txt(self):
        self.report_rate_price_txt = num2text(int(self.report_rate_price), main_units=((u'сум', u'сумы', u'сум'), 'f'))
        return self.report_rate_price_txt


class Images(models.Model):
    image_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    image = models.ImageField(blank=True, null=True, verbose_name='Фото')
    report = models.ForeignKey('Report', on_delete=models.CASCADE, blank=True, null=True, related_name='reportImages',
                               verbose_name='Отчёт')

    # def save(self, *args, **kwargs):
    #     self.objects.create(something=kwargs['something'])
    #     super(Images, self).save(*args, **kwargs)


class PassportPhotos(models.Model):
    p_photo_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    photo = models.ImageField(blank=True, null=True, verbose_name='Фото пасспорта')
    report = models.ForeignKey('Report', on_delete=models.CASCADE, blank=True, null=True, related_name='reportPPhotos',
                               verbose_name='Отчёт')


class OtherPhotos(models.Model):
    o_photo_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    photos = models.ImageField(blank=True, null=True, verbose_name='Фото чеков')
    report = models.ForeignKey('Report', on_delete=models.CASCADE, blank=True, null=True, related_name='reportOPhotos',
                               verbose_name='Отчёт')


class Checks(models.Model):
    checks_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    checks = models.ImageField(blank=True, null=True, verbose_name='Фото чеков')
    report = models.ForeignKey('Report', on_delete=models.CASCADE, blank=True, null=True, related_name='reportChecks',
                               verbose_name='Отчёт')


class Report(models.Model):
    report_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    report_number = models.CharField(max_length=10)
    report_date = models.CharField(max_length=10)
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='created_by', verbose_name='Создан')
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
    key = models.CharField(max_length=8, blank=True)

    total_report_cost = models.CharField(max_length=15)
    total_report_cost_txt = models.CharField(max_length=200)

    pdf_report = models.FileField(blank=True, null=True, upload_to='uploads/%Y/%m/%d/', verbose_name='Отчёт в пдф')
    pdf_report_base64 = models.CharField(max_length=1000000, blank=True, null=True)
    pdf_report_pkcs7 = models.JSONField(blank=True, null=True)
    pdf_report_qr = models.JSONField(blank=True, null=True)
    pdf_qr_code = models.CharField(max_length = 500, blank = True, null= True)
    
    passport_photo = models.FileField(blank=True, null=True, verbose_name='Фото пасспорта')
    registration_photo = models.FileField(blank=True, null=True, verbose_name='Фото тех.пасспорта')

    wear_data = models.JSONField(blank=True, null=True)
    service_data = models.JSONField(blank=True, null=True)
    product_data = models.JSONField(blank=True, null=True)
    consumable_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return str(self.report_id)

    def get_product_acc_cost(self):
        print('get_product_acc_cost')
        self.product_acc_cost = (self.product_cost * (1 - self.wear_data.__getitem__('accept_wear') / 100))
        return self.product_acc_cost

    def get_total_report_price(self):
        print('get_total_report_price')
        self.total_report_cost = ' '.join(
            '{:,}'.format(int(self.service_cost + self.get_product_acc_cost() + self.consumable_cost)).split(','))

    def get_total_report_cost_txt(self):
        self.total_report_cost_txt = num2text(int(self.service_cost + self.get_product_acc_cost() + self.consumable_cost), main_units=((u'сум', u'сумы', u'суммов'), 'f'))
        return self.total_report_cost_txt

    def set_private_key(self):
        self.key = str(self.report_id)[0] + self.car.car_number[2] + self.car.car_number[7] + self.car.car_number[5] + \
                   str(self.contract_id)[0] + str(self.car.release_date)[2] + str(self.car.release_date)[3] + \
                   self.car.brand[0]

    class Meta:
        verbose_name = 'Отчёт'
        verbose_name_plural = 'Отчёты'
