from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from simple_history.models import HistoricalRecords
from django.core.validators import MinValueValidator, MaxValueValidator



class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class MyUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        ('owner', 'Собственник'),
        ('organizer', 'Организатор'),
        ('executor', 'Исполнитель'),
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    author_name = models.CharField(max_length=255, blank=True, null=True)  # Поле для хранения имени автора
    history = HistoricalRecords()  # Поле для отслеживания истории изменений

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

    def save(self, *args, **kwargs):
        if 'author' in kwargs and kwargs['author']:
            author = kwargs.pop('author')
            if not self.author_name:
                self.author_name = author.get_full_name() or author.email
        super().save(*args, **kwargs)

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from simple_history.models import HistoricalRecords

# Получение пользовательской модели
User = get_user_model()

class PositionDirectory(models.Model):
    position = models.CharField(max_length=255)  # Поле для хранения названия должности
    comments = models.TextField(blank=True, null=True)  # Поле для хранения комментариев, может быть пустым
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Поле для хранения ссылки на автора
    author_name = models.CharField(max_length=255, blank=True, null=True)  # Поле для хранения имени автора

    def save(self, *args, **kwargs):
        # Если автор установлен и поле author_name еще не заполнено
        if self.author and not self.author_name:
            # Сохранить полное имя автора или его email
            self.author_name = self.author.get_full_name() or self.author.email
        # Вызов стандартного метода save для сохранения изменений
        super().save(*args, **kwargs)

    def __str__(self):
        # Отображение названия должности при вызове str()
        return self.position

class TariffDirectory(models.Model):
    tariff_name = models.CharField(max_length=255)  # Поле для хранения названия тарифа
    cost_per_minute = models.DecimalField(max_digits=10, decimal_places=2)  # Поле для хранения стоимости минуты рабочего времени
    comments = models.TextField(blank=True, null=True)  # Поле для хранения комментариев, может быть пустым
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Поле для хранения ссылки на автора
    author_name = models.CharField(max_length=255, blank=True, null=True)  # Поле для хранения имени автора
    history = HistoricalRecords()  # Поле для хранения истории изменений

    def save(self, *args, **kwargs):
        # Если автор установлен и поле author_name еще не заполнено
        if self.author and not self.author_name:
            # Сохранить полное имя автора или его email
            self.author_name = self.author.get_full_name() or self.author.email
        # Вызов стандартного метода save для сохранения изменений
        super().save(*args, **kwargs)

    def __str__(self):
        # Отображение названия тарифа при вызове str()
        return self.tariff_name





# Модель штатного расписания
from simple_history.models import HistoricalRecords

class StaffSchedule(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    user_name = models.CharField(max_length=255, null=True, blank=True)  # Поле для хранения имени пользователя
    position = models.ForeignKey(PositionDirectory, on_delete=models.CASCADE)  # Поле для связи с моделью PositionDirectory
    tariff = models.ForeignKey(TariffDirectory, on_delete=models.CASCADE)  # Поле для связи с моделью TariffDirectory
    quantity = models.IntegerField()  # Поле для хранения количества работников
    norm_time_per_month = models.IntegerField()  # Поле для хранения нормы времени в месяц на одного человека (в минутах)
    total_working_time = models.IntegerField(editable=False)  # Поле для хранения общего рабочего времени (рассчитывается автоматически)
    total_salary_fund = models.DecimalField(max_digits=15, decimal_places=2, editable=False)  # Поле для хранения фонда оплаты труда (рассчитывается автоматически)
    history = HistoricalRecords()  # Поле для хранения истории изменений

    # Метод для сохранения модели с расчетом total_working_time и total_salary_fund
    def save(self, *args, **kwargs):
        if self.user:
            self.user_name = self.user.get_full_name() or self.user.email  # Сохраняем имя или email пользователя
        self.total_working_time = self.quantity * self.norm_time_per_month  # Расчет общего рабочего времени
        self.total_salary_fund = self.total_working_time * self.tariff.cost_per_minute  # Расчет фонда оплаты труда
        super().save(*args, **kwargs)  # Вызов родительского метода save()

    def __str__(self):
        return f"{self.position} - {self.quantity}"  # Отображение должности и количества при вызове str()

    class Meta:
        # Ограничения для полей quantity и norm_time_per_month
        constraints = [
            models.CheckConstraint(check=models.Q(quantity__gte=1) & models.Q(quantity__lte=1000), name='quantity_range'),
            models.CheckConstraint(check=models.Q(norm_time_per_month__gte=1) & models.Q(norm_time_per_month__lte=44000), name='norm_time_per_month_range'),  # Обновлено максимальное значение
        ]


from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords

# Модель для справочника должностей организаторов
class OrganizerPositionDirectory(models.Model):
    position = models.CharField(max_length=255)  # Поле для хранения названия должности
    comments = models.TextField(blank=True, null=True)  # Поле для хранения комментариев, может быть пустым
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)  # Поле для хранения ссылки на автора
    author_name = models.CharField(max_length=255, blank=True, null=True)  # Поле для хранения имени автора

    def save(self, *args, **kwargs):
        # Если автор установлен и поле author_name еще не заполнено
        if self.author and not self.author_name:
            # Сохранить полное имя автора или его email
            self.author_name = self.author.get_full_name() or self.author.email
        # Вызов стандартного метода save
        super().save(*args, **kwargs)

    def __str__(self):
        return self.position  # Отображение названия должности при вызове str()


# Модель для тарифов организаторов
class OrganizerTariff(models.Model):
    position = models.OneToOneField(OrganizerPositionDirectory, on_delete=models.CASCADE)  # Связь с моделью OrganizerPositionDirectory
    rate = models.DecimalField(
        max_digits=4,
        decimal_places=3,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]  # Поле для хранения норматива с проверкой значений от 0.0 до 1.0
    )
    base = models.TextField()  # Поле для хранения базы
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)  # Поле для хранения ссылки на автора
    author_name = models.CharField(max_length=255, blank=True, null=True)  # Поле для хранения имени автора
    history = HistoricalRecords()  # Поле для отслеживания истории изменений

    def save(self, *args, **kwargs):
        # Если автор установлен и поле author_name еще не заполнено
        if self.author and not self.author_name:
            # Сохранить полное имя автора или его email
            self.author_name = self.author.get_full_name() or self.author.email
        # Вызов стандартного метода save
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.position.position} - {self.rate}'  # Отображение информации о тарифе при вызове str()






from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords

class TaxSystem(models.Model):
    name = models.CharField(max_length=255)  # Поле для хранения названия системы налогообложения
    comments = models.TextField(blank=True, null=True)  # Поле для хранения комментариев, может быть пустым
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)  # Поле для хранения ссылки на автора
    author_name = models.CharField(max_length=255, blank=True, null=True)  # Поле для хранения имени автора
    history = HistoricalRecords()  # Поле для отслеживания истории изменений

    def save(self, *args, **kwargs):
        if self.author and not self.author_name:
            self.author_name = self.author.get_full_name() or self.author.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name  # Отображение названия системы налогообложения при вызове str()


from django.contrib.auth import get_user_model
from django.db import models
from simple_history.models import HistoricalRecords

# Получение пользовательской модели
User = get_user_model()


class Client(models.Model):
    short_name = models.CharField(max_length=255, blank=False)  # Поле для краткого наименования
    full_name = models.TextField(blank=True)  # Поле для полного наименования
    contract_price = models.IntegerField(blank=False)  # Поле для цены договора
    contract_number_date = models.TextField(blank=True)  # Поле для номера и даты договора
    inn = models.CharField(max_length=12, blank=True)  # Поле для ИНН
    tax_system = models.ForeignKey('TaxSystem', on_delete=models.CASCADE)  # Поле для системы налогообложения, обязательно для заполнения
    nomenclature_units = models.IntegerField(blank=False, default=0)  # Поле для количества номенклатурных единиц
    activity_types = models.TextField(blank=True)  # Поле для видов деятельности
    contact_name = models.CharField(max_length=255, blank=True)  # Поле для имени контакта
    phone_number = models.CharField(max_length=15, blank=True)  # Поле для номера телефона
    email = models.EmailField(blank=True)  # Поле для email
    postal_address = models.TextField(blank=True)  # Поле для почтового адреса
    comment = models.TextField(blank=True)  # Поле для комментариев
    hide_in_list = models.BooleanField(default=False)  # Поле для скрытия в списке (по умолчанию не скрыто)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Поле для хранения ссылки на автора
    author_name = models.CharField(max_length=255, blank=True, null=True)  # Поле для хранения имени автора
    history = HistoricalRecords()  # Поле для отслеживания истории изменений

    def save(self, *args, **kwargs):
        # Если автор установлен и поле author_name еще не заполнено
        if self.author and not self.author_name:
            # Сохранить полное имя автора или его email
            self.author_name = self.author.get_full_name() or self.author.email
        # Вызов стандартного метода save
        super().save(*args, **kwargs)

    def __str__(self):
        # Отображение краткого наименования при вызове str()
        return self.short_name
