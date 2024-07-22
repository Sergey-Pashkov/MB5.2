from django.urls import path, include  # Импорт для создания маршрутов
from django.views.generic import TemplateView  # Импорт для отображения статических страниц
from .views import (  # Импорт всех нужных представлений
    LoginView, DashboardRedirectView, OwnerDashboardView, OrganizerDashboardView, ExecutorDashboardView,
    PositionDirectoryListView, PositionDirectoryDetailView, PositionDirectoryCreateView,
    PositionDirectoryUpdateView, PositionDirectoryDeleteView,
    TariffDirectoryListView, TariffDirectoryDetailView, TariffDirectoryCreateView,
    TariffDirectoryUpdateView, TariffDirectoryDeleteView,
    StaffScheduleListView, StaffScheduleDetailView, StaffScheduleCreateView,
    StaffScheduleUpdateView, StaffScheduleDeleteView,
    OrganizerPositionDirectoryListView, OrganizerPositionDirectoryCreateView, OrganizerPositionDirectoryDetailView,
    OrganizerPositionDirectoryUpdateView, OrganizerPositionDirectoryDeleteView,
    OrganizerTariffListView, OrganizerTariffCreateView, OrganizerTariffDetailView,
    OrganizerTariffUpdateView, OrganizerTariffDeleteView,
    ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView, export_clients,
    TaxSystemListView, TaxSystemCreateView, TaxSystemDetailView, TaxSystemUpdateView, TaxSystemDeleteView,
    worktypegroup_list, worktypegroup_create, worktypegroup_edit, worktypegroup_delete,
    worktype_list, worktype_create, worktype_edit, worktype_delete, worktype_view, export_worktypes_to_excel, worktype_history, worktype_revert,
    StandardOperationsJournalListView, StandardOperationsJournalCreateView, StandardOperationsJournalUpdateView, StandardOperationsJournalDeleteView, StandardOperationsJournalDetailView,
)
from django.http import JsonResponse
from .models import WorkType 
from django.urls import path
from . import views  # Импортируем представления из текущего модуля


urlpatterns = [
    path('positions/', PositionDirectoryListView.as_view(), name='positions_list'),  # Список должностей
    path('positions/new/', PositionDirectoryCreateView.as_view(), name='position_create'),  # Создание новой должности
    path('positions/<int:pk>/', PositionDirectoryDetailView.as_view(), name='position_detail'),  # Просмотр деталей должности
    path('positions/<int:pk>/edit/', PositionDirectoryUpdateView.as_view(), name='position_edit'),  # Редактирование должности
    path('positions/<int:pk>/delete/', PositionDirectoryDeleteView.as_view(), name='position_delete'),  # Удаление должности

    path('tariffs/', TariffDirectoryListView.as_view(), name='tariffs_list'),  # Список тарифов
    path('tariffs/new/', TariffDirectoryCreateView.as_view(), name='tariff_create'),  # Создание нового тарифа
    path('tariffs/<int:pk>/', TariffDirectoryDetailView.as_view(), name='tariff_detail'),  # Просмотр деталей тарифа
    path('tariffs/<int:pk>/edit/', TariffDirectoryUpdateView.as_view(), name='tariff_edit'),  # Редактирование тарифа
    path('tariffs/<int:pk>/delete/', TariffDirectoryDeleteView.as_view(), name='tariff_delete'),  # Удаление тарифа

    path('staff-schedule/', StaffScheduleListView.as_view(), name='staff_schedule_list'),  # Список расписаний сотрудников
    path('staff-schedule/new/', StaffScheduleCreateView.as_view(), name='staff_schedule_create'),  # Создание нового расписания
    path('staff-schedule/<int:pk>/', StaffScheduleDetailView.as_view(), name='staff_schedule_detail'),  # Просмотр деталей расписания
    path('staff-schedule/<int:pk>/edit/', StaffScheduleUpdateView.as_view(), name='staff_schedule_edit'),  # Редактирование расписания
    path('staff-schedule/<int:pk>/delete/', StaffScheduleDeleteView.as_view(), name='staff_schedule_delete'),  # Удаление расписания

    path('forbidden/', TemplateView.as_view(template_name='forbidden.html'), name='forbidden'),  # Страница для уведомления о недостаточности прав доступа

    path('login/', LoginView.as_view(), name='login'),  # Страница входа
    path('dashboard/', DashboardRedirectView.as_view(), name='dashboard_redirect'),  # Редирект на дашборд
    path('dashboard/owner/', OwnerDashboardView.as_view(), name='owner_dashboard'),  # Дашборд собственника
    path('dashboard/organizer/', OrganizerDashboardView.as_view(), name='organizer_dashboard'),  # Дашборд организатора
    path('dashboard/executor/', ExecutorDashboardView.as_view(), name='executor_dashboard'),  # Дашборд исполнителя

    path('organizer_positions/', OrganizerPositionDirectoryListView.as_view(), name='organizer_positions_list'),  # Список должностей организаторов
    path('organizer_positions/new/', OrganizerPositionDirectoryCreateView.as_view(), name='organizer_position_create'),  # Создание новой должности организатора
    path('organizer_positions/<int:pk>/', OrganizerPositionDirectoryDetailView.as_view(), name='organizer_position_detail'),  # Просмотр деталей должности организатора
    path('organizer_positions/<int:pk>/edit/', OrganizerPositionDirectoryUpdateView.as_view(), name='organizer_position_edit'),  # Редактирование должности организатора
    path('organizer_positions/<int:pk>/delete/', OrganizerPositionDirectoryDeleteView.as_view(), name='organizer_position_delete'),  # Удаление должности организатора

    path('organizer_tariffs/', OrganizerTariffListView.as_view(), name='organizer_tariffs_list'),  # Список тарифов организаторов
    path('organizer_tariffs/new/', OrganizerTariffCreateView.as_view(), name='organizer_tariff_create'),  # Создание нового тарифа организатора
    path('organizer_tariffs/<int:pk>/', OrganizerTariffDetailView.as_view(), name='organizer_tariff_detail'),  # Просмотр деталей тарифа организатора
    path('organizer_tariffs/<int:pk>/edit/', OrganizerTariffUpdateView.as_view(), name='organizer_tariff_edit'),  # Редактирование тарифа организатора
    path('organizer_tariffs/<int:pk>/delete/', OrganizerTariffDeleteView.as_view(), name='organizer_tariff_delete'),  # Удаление тарифа организатора

    path('tax_systems/', TaxSystemListView.as_view(), name='tax_systems_list'),  # Список систем налогообложения
    path('tax_systems/new/', TaxSystemCreateView.as_view(), name='tax_system_create'),  # Создание новой системы налогообложения
    path('tax_systems/<int:pk>/', TaxSystemDetailView.as_view(), name='tax_system_detail'),  # Просмотр деталей системы налогообложения
    path('tax_systems/<int:pk>/edit/', TaxSystemUpdateView.as_view(), name='tax_system_edit'),  # Редактирование системы налогообложения
    path('tax_systems/<int:pk>/delete/', TaxSystemDeleteView.as_view(), name='tax_system_delete'),  # Удаление системы налогообложения

    path('clients/', ClientListView.as_view(), name='client_list'),  # Список клиентов
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),  # Просмотр деталей клиента
    path('clients/new/', ClientCreateView.as_view(), name='client_create'),  # Создание нового клиента
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='client_edit'),  # Редактирование клиента
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),  # Удаление клиента
    path('export_clients/', export_clients, name='export_clients'),  # Экспорт клиентов в Excel

    path('worktypegroups/', worktypegroup_list, name='worktypegroup_list'),  # Список групп видов работ
    path('worktypegroups/create/', worktypegroup_create, name='worktypegroup_create'),  # Создание новой группы видов работ
    path('worktypegroups/edit/<int:pk>/', worktypegroup_edit, name='worktypegroup_edit'),  # Редактирование группы видов работ
    path('worktypegroups/delete/<int:pk>/', worktypegroup_delete, name='worktypegroup_delete'),  # Удаление группы видов работ

    path('worktypes/', worktype_list, name='worktype_list'),  # Список видов работ
    path('worktypes/create/', worktype_create, name='worktype_create'),  # Создание нового вида работ
    path('worktypes/edit/<int:pk>/', worktype_edit, name='worktype_edit'),  # Редактирование вида работ
    path('worktypes/delete/<int:pk>/', worktype_delete, name='worktype_delete'),  # Удаление вида работ

    path('worktypes/view/<int:pk>/', worktype_view, name='worktype_view'),  # Просмотр вида работ
    path('worktypes/export/', export_worktypes_to_excel, name='worktype_export'),  # Экспорт видов работ в Excel
    path('worktypes/history/', worktype_history, name='worktype_history'),  # История изменений видов работ за последние 30 дней
    path('worktypes/revert/<int:pk>/<int:history_id>/', worktype_revert, name='worktype_revert'),  # Откат к предыдущей версии вида работ

    path('journals/', StandardOperationsJournalListView.as_view(), name='journal_list'),  # Список стандартных операций
    path('journals/create/', StandardOperationsJournalCreateView.as_view(), name='journal_create'),  # Создание новой стандартной операции
    path('journals/update/<int:pk>/', StandardOperationsJournalUpdateView.as_view(), name='journal_update'),  # Редактирование стандартной операции
    path('journals/delete/<int:pk>/', StandardOperationsJournalDeleteView.as_view(), name='journal_delete'),  # Удаление стандартной операции
    path('journals/<int:pk>/', StandardOperationsJournalDetailView.as_view(), name='journal_detail'),  # Добавьте этот маршрут

    path('ajax/get-work-type-group/', views.get_work_type_group, name='get_work_type_group'),
    # Добавляем URL для обработки AJAX-запроса для получения данных группы работы
]
