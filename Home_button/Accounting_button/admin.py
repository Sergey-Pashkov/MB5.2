from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser
from simple_history.admin import SimpleHistoryAdmin


class MyUserAdmin(UserAdmin):
    model = MyUser
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active', 'author_name')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name','user_type', 'author_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),  # Убедитесь, что здесь указаны только существующие поля
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'user_type','is_staff', 'is_active', 'author_name')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    

    def save_model(self, request, obj, form, change):
        obj.save(author=request.user)

admin.site.register(MyUser, MyUserAdmin)



from django.contrib import admin
from .models import PositionDirectory, TariffDirectory, StaffSchedule

# Регистрация модели PositionDirectory в админке
@admin.register(PositionDirectory)
class PositionDirectoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'comments')  # Поля, которые будут отображаться в списке объектов

# Регистрация модели TariffDirectory в админке
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import TariffDirectory

@admin.register(TariffDirectory)
class TariffDirectoryAdmin(SimpleHistoryAdmin):
    list_display = ('tariff_name', 'cost_per_minute', 'comments')





# Регистрация модели StaffSchedule в админке
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import StaffSchedule

@admin.register(StaffSchedule)
class StaffScheduleAdmin(SimpleHistoryAdmin):
    list_display = ('position', 'tariff', 'quantity', 'norm_time_per_month', 'total_working_time', 'total_salary_fund')  # Поля, которые будут отображаться в списке объектов
    readonly_fields = ('total_working_time', 'total_salary_fund')  # Поля, которые будут отображаться как только для чтения

# Альтернативный способ регистрации моделей в админке (более простой, без настройки админских классов)
# admin.site.register(PositionDirectory)
# admin.site.register(TariffDirectory)
# admin.site.register(StaffSchedule)

from django.contrib import admin
from .models import OrganizerPositionDirectory, OrganizerTariff

# Регистрация модели OrganizerPositionDirectory в админке
admin.site.register(OrganizerPositionDirectory)

# Регистрация модели OrganizerTariff в админке
@admin.register(OrganizerTariff)
class OrganizerTariffAdmin(admin.ModelAdmin):
    list_display = ('position', 'rate', 'base')
    search_fields = ('position__position',)


from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import TaxSystem

@admin.register(TaxSystem)
class TaxSystemAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'comments')
    search_fields = ('name',)



from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import WorkTypeGroup

# Регистрация модели WorkTypeGroup с использованием SimpleHistoryAdmin для отслеживания истории изменений
@admin.register(WorkTypeGroup)
class WorkTypeGroupAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'author', 'hide_in_list')  # Поля, отображаемые в списке
    search_fields = ('name', 'author__email')  # Поля, по которым можно искать
    list_filter = ('hide_in_list',)  # Поля для фильтрации

    # Автоматическое заполнение поля author_name на основе автора
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        if not obj.author_name:
            obj.author_name = obj.author.get_full_name() or obj.author.email
        super().save_model(request, obj, form, change)
