# Accounting_button/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

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

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name


from django.db import models
from django.conf import settings

# Модель справочника должностей исполнителей
class PositionDirectory(models.Model):
    position = models.CharField(max_length=255)  # Поле для хранения названия должности
    comments = models.TextField(blank=True, null=True)  # Поле для хранения комментариев, может быть пустым

    def __str__(self):
        return self.position  # Отображение названия должности при вызове str()

# Модель справочника тарифов исполнителей
from django.db import models
from simple_history.models import HistoricalRecords

class TariffDirectory(models.Model):
    tariff_name = models.CharField(max_length=255)  # Поле для хранения названия тарифа
    cost_per_minute = models.DecimalField(max_digits=10, decimal_places=2)  # Поле для хранения стоимости минуты рабочего времени
    comments = models.TextField(blank=True, null=True)  # Поле для хранения комментариев, может быть пустым
    history = HistoricalRecords()  # Поле для хранения истории изменений

    def __str__(self):
        return self.tariff_name  # Отображение названия тарифа при вызове str()


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

# Модель для справочника должностей организаторов
class OrganizerPositionDirectory(models.Model):
    position = models.CharField(max_length=255)  # Поле для хранения названия должности
    comments = models.TextField(blank=True, null=True)  # Поле для хранения комментариев, может быть пустым

    def __str__(self):
        return self.position  # Отображение названия должности при вызове str()
