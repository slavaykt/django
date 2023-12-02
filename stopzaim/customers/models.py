from django.db import models
import datetime

gender_choices = [('male', 'муж'), ('female', 'жен')]
currency_choices = [('rur', 'руб.')]
property_type_choices = [('individual', 'Индивидуальная'), ('joint', 'Общая совместная')]

class Company(models.Model):
    name = models.CharField('Наименование',max_length=255)
    def __str__(self):
        return self.name

class Customer(models.Model):
    first_name = models.CharField('Имя', max_length=50, default='')
    middle_name = models.CharField('Отчество', max_length=50, default='')
    surname = models.CharField('Фамилия', max_length=50, default='')
    gender = models.CharField('Пол', max_length=6, choices=gender_choices, default='male')
    birthdate = models.DateField('Дата рождения', default=datetime.date.today)
    phone = models.CharField('Телефон', max_length=20, default='')
    tax_id = models.CharField('ИНН', max_length=12, default='')
    snils = models.CharField('СНИЛС', max_length=11, default='')
    passport_series = models.CharField('серия', max_length=5, default='')
    passport_number = models.CharField('номер', max_length=6, default='')
    passport_issuer = models.CharField('кем выдан', max_length=100, default='')
    passport_issue_date = models.DateField('дата выдачи', default=datetime.date.today)
    passport_issuer_code = models.CharField('код подразделения', max_length=6, default='')
    address = models.CharField('Адрес', max_length=255, default='')
    birthplace = models.CharField('Место рождения', max_length=255, default='')
    tax_inspection = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Налоговая', related_name='customer_tax_inspection', default=None)
    occupation_choices = [('employed', 'Работает'), ('unemployed', 'Безработный'), ('pensioner', 'Пенсионер'), ('employed_pensioner', 'Работающий пенсионер')]
    occupation = models.CharField('Место работы', max_length=50, choices=occupation_choices, default='unemployed')
    previous_year_income = models.FloatField('Доход за прошлый год', default=0)
    job = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Место работы', related_name='customer_job', default=None)
    position = models.CharField('Должность', max_length=100, default='')
    sro = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE, verbose_name='СРО', related_name='customer_sro', default=None)
    arbitration_court = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Арбитражный суд', related_name='customer_arbitration_court', default=None)
    gosuslugi = models.CharField('Госуслуги', max_length=50, default='')
    application_date = models.DateField('Дата подачи заявления', default=datetime.date.today)
    is_married = models.BooleanField('Состоит в браке',default=False)
    spouse_name = models.CharField('ФИО супруга (-и)', max_length=100, default='')
    comments = models.TextField('Комментарий', max_length=1000, default='')

    def __str__(self):
        return f"{self.surname} {self.first_name} {self.middle_name}"
    
class CustomerChild(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    name = models.CharField('ФИО',max_length=255, default='')
    gender = models.CharField('Пол', max_length=6, choices=gender_choices, default='male')
    birthdate = models.DateField('Дата рождения', default=datetime.date.today)

class CustomerBankAccount(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    account_type_choices = [('deposit', 'вклад'), ('current', 'текущий')]
    type = models.CharField('Вид счета', max_length=10, choices=account_type_choices, default='current')
    currency = models.CharField('Валюта счета', max_length=10, choices=currency_choices, default='rur')
    account_number = models.CharField('Номер счета',max_length=20, default='')
    bank = models.ForeignKey(Company,blank=True,null=True,on_delete=models.CASCADE, verbose_name='Банк')
    balance = models.FloatField('Сумма',default=0)
    opening_date = models.DateField('Дата открытия', default=datetime.date.today)

class CustomerPayable(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    payable_type_choices = [('credit', 'кредит'), ('loan', 'заeм'), ('credit_card', 'кредитная карта'), ('utilities', 'коммунальные услуги'), ('tax', 'налог')]
    type = models.CharField('Вид счета', max_length=30, choices=payable_type_choices, default='credit')
    lender = models.ForeignKey(Company,blank=True,null=True,on_delete=models.CASCADE, verbose_name='Кредитор')
    basis = models.CharField('Основание возникновения',max_length=255, default='')
    gross_amount = models.FloatField('Сумма всего',default=0)
    net_amount = models.FloatField('в т.ч. задолженность',default=0)
    penalties_amount = models.FloatField('в т.ч. штрафы, пени',default=0)

class CustomerExecutiveDoc(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    executive_doc_choices = [('resolution', 'постановление'), ('court_order', 'судебный приказ'), ('execution_writ', 'исполнительный лист')]
    type = models.CharField('Вид документа', max_length=30, choices=executive_doc_choices, default='resolution')
    date = models.DateField('Дата', default=datetime.date.today)
    doc_number = models.CharField('Номер',max_length=20, default='')
    executor = models.CharField('Исполнитель',max_length=100, default='')
    content = models.CharField('Содержание',max_length=255, default='')

class CustomerMandatoryPayment(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    tax_name_choices = [('transport_tax', 'транспортный налог'), ('land_tax', 'земельный налог'), ('property_tax', 'налог на имущество')]
    tax_name = models.CharField('Наименование налога (сбора)',max_length=100, choices=tax_name_choices, default='transport_tax')
    arrears_amount = models.FloatField('Недоимка',default=0)
    penalties_amount = models.FloatField('Штрафы, пени',default=0)

class CustomerRealty(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    name = models.CharField('Наименование',max_length=255, default='')
    realty_type_choices = [('land_plot', 'Земельный участок'), ('house', 'Жилой дом, дача'), ('apartment', 'Квартира'), ('garage', 'Гараж'), ('other', 'Иное недвижимое имущество')]
    type = models.CharField('Вид имущества', max_length=30, choices=realty_type_choices, default='apartment')
    property_type = models.CharField('Вид собственности', max_length=30, choices=property_type_choices, default='individual')
    area = models.FloatField('Площадь',default=0)
    acquiring_basis = models.CharField('Основание приобретения',max_length=255, default='')
    pledge = models.CharField('Сведения о залоге',max_length=100, default='')
    address = models.CharField('Адрес', max_length=255, default='')

class CustomerTransport(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    name = models.CharField('Наименование',max_length=255, default='')
    transport_type_choices = [('car', 'Автомобиль легковой'), ('truck', 'Автомобиль грузовой'), ('motobike', 'Мототранспортное средство'), 
                              ('agriculturtal_machinery', 'Сельскохозяйственная техника'), ('boat', 'Водный транспорт'), 
                              ('plane', 'Воздушный транспорт'), ('other', 'Иное транспортное средство')]
    type = models.CharField('Вид имущества', max_length=30, choices=transport_type_choices, default='car')
    property_type = models.CharField('Вид собственности', max_length=30, choices=property_type_choices, default='individual')
    cost = models.FloatField('Стоимость',default=0)  
    production_year = models.CharField('Год выпуска',max_length=4, default='')
    plate_number = models.CharField('Основание приобретения',max_length=20, default='')
    pledge = models.CharField('Сведения о залоге',max_length=100, default='')
    address = models.CharField('Адрес', max_length=255, default='')

class CustomerLoan(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    company = models.ForeignKey(Company,blank=True,null=True,on_delete=models.CASCADE, verbose_name='Кредитор')
    amount = models.FloatField('Сумма',default=0)
