from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser
from simple_history.admin import SimpleHistoryAdmin


class MyUserAdmin(UserAdmin):
    model = MyUser
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'user_type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

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


