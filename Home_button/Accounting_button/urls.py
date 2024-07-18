# Accounting_button/urls.py

from django.urls import path
from .views import LoginView, DashboardRedirectView, OwnerDashboardView, OrganizerDashboardView, ExecutorDashboardView
from django.views.generic import TemplateView
from .views import (
    PositionDirectoryListView, PositionDirectoryDetailView, PositionDirectoryCreateView,
    PositionDirectoryUpdateView, PositionDirectoryDeleteView,
    TariffDirectoryListView, TariffDirectoryDetailView, TariffDirectoryCreateView,
    TariffDirectoryUpdateView, TariffDirectoryDeleteView,
    StaffScheduleListView, StaffScheduleDetailView, StaffScheduleCreateView,
    StaffScheduleUpdateView, StaffScheduleDeleteView,
    OrganizerPositionDirectoryListView,
    OrganizerPositionDirectoryCreateView,
    OrganizerPositionDirectoryDetailView,
    OrganizerPositionDirectoryUpdateView,
    OrganizerPositionDirectoryDeleteView,
    OwnerDashboardView,
    TaxSystemListView,
    TaxSystemCreateView,
    TaxSystemDetailView,
    TaxSystemUpdateView,
    TaxSystemDeleteView
  
)
from django.urls import path
from .views import OrganizerTariffListView, OrganizerTariffCreateView, OrganizerTariffDetailView, OrganizerTariffUpdateView, OrganizerTariffDeleteView

from .views import ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView 

from django.urls import path
from .views import ClientListView, export_clients

from django.urls import path
from . import views 

urlpatterns = [
    path('positions/', PositionDirectoryListView.as_view(), name='positions_list'),
    path('positions/new/', PositionDirectoryCreateView.as_view(), name='position_create'),
    path('positions/<int:pk>/', PositionDirectoryDetailView.as_view(), name='position_detail'),
    path('positions/<int:pk>/edit/', PositionDirectoryUpdateView.as_view(), name='position_edit'),
    path('positions/<int:pk>/delete/', PositionDirectoryDeleteView.as_view(), name='position_delete'),

    path('tariffs/', TariffDirectoryListView.as_view(), name='tariffs_list'),
    path('tariffs/new/', TariffDirectoryCreateView.as_view(), name='tariff_create'),
    path('tariffs/<int:pk>/', TariffDirectoryDetailView.as_view(), name='tariff_detail'),
    path('tariffs/<int:pk>/edit/', TariffDirectoryUpdateView.as_view(), name='tariff_edit'),
    path('tariffs/<int:pk>/delete/', TariffDirectoryDeleteView.as_view(), name='tariff_delete'),

    path('staff-schedule/', StaffScheduleListView.as_view(), name='staff_schedule_list'),
    path('staff-schedule/new/', StaffScheduleCreateView.as_view(), name='staff_schedule_create'),
    path('staff-schedule/<int:pk>/', StaffScheduleDetailView.as_view(), name='staff_schedule_detail'),
    path('staff-schedule/<int:pk>/edit/', StaffScheduleUpdateView.as_view(), name='staff_schedule_edit'),
    path('staff-schedule/<int:pk>/delete/', StaffScheduleDeleteView.as_view(), name='staff_schedule_delete'),

    # Страница для уведомления о недостаточности прав доступа
    path('forbidden/', TemplateView.as_view(template_name='forbidden.html'), name='forbidden'),

    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/', DashboardRedirectView.as_view(), name='dashboard_redirect'),
    path('dashboard/owner/', OwnerDashboardView.as_view(), name='owner_dashboard'),
    path('dashboard/organizer/', OrganizerDashboardView.as_view(), name='organizer_dashboard'),
    path('dashboard/executor/', ExecutorDashboardView.as_view(), name='executor_dashboard'),

    path('owner/dashboard/', OwnerDashboardView.as_view(), name='owner_dashboard'),  # Маршрут для дашборда собственника
    path('organizer_positions/', OrganizerPositionDirectoryListView.as_view(), name='organizer_positions_list'),  # URL для списка должностей
    path('organizer_positions/new/', OrganizerPositionDirectoryCreateView.as_view(), name='organizer_position_create'),  # URL для создания новой должности
    path('organizer_positions/<int:pk>/', OrganizerPositionDirectoryDetailView.as_view(), name='organizer_position_detail'),  # URL для просмотра деталей должности
    path('organizer_positions/<int:pk>/edit/', OrganizerPositionDirectoryUpdateView.as_view(), name='organizer_position_edit'),  # URL для редактирования должности
    path('organizer_positions/<int:pk>/delete/', OrganizerPositionDirectoryDeleteView.as_view(), name='organizer_position_delete'),  # URL для удаления должности

    # URL для списка тарифов организаторов
    path('organizer_tariffs/', OrganizerTariffListView.as_view(), name='organizer_tariffs_list'),
    
    # URL для создания нового тарифа
    path('organizer_tariffs/new/', OrganizerTariffCreateView.as_view(), name='organizer_tariff_create'),
    
    # URL для просмотра деталей тарифа
    path('organizer_tariffs/<int:pk>/', OrganizerTariffDetailView.as_view(), name='organizer_tariff_detail'),
    
    # URL для редактирования тарифа
    path('organizer_tariffs/<int:pk>/edit/', OrganizerTariffUpdateView.as_view(), name='organizer_tariff_edit'),
    
    # URL для удаления тарифа
    path('organizer_tariffs/<int:pk>/delete/', OrganizerTariffDeleteView.as_view(), name='organizer_tariff_delete'),

    path('tax_systems/', TaxSystemListView.as_view(), name='tax_systems_list'),
    path('tax_systems/new/', TaxSystemCreateView.as_view(), name='tax_system_create'),
    path('tax_systems/<int:pk>/', TaxSystemDetailView.as_view(), name='tax_system_detail'),
    path('tax_systems/<int:pk>/edit/', TaxSystemUpdateView.as_view(), name='tax_system_edit'),
    path('tax_systems/<int:pk>/delete/', TaxSystemDeleteView.as_view(), name='tax_system_delete'),

    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('clients/new/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='client_edit'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),

  # выгрузка списка клиентов в эксель
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('export_clients/', export_clients, name='export_clients'),
  
    path('', views.worktypegroup_list, name='worktypegroup_list'),
    path('create/', views.worktypegroup_create, name='worktypegroup_create'),
    path('edit/<int:pk>/', views.worktypegroup_edit, name='worktypegroup_edit'),
    path('delete/<int:pk>/', views.worktypegroup_delete, name='worktypegroup_delete'),

    path('worktypes/', views.worktype_list, name='worktype_list'),  # URL для отображения списка видов работ
    path('worktypes/create/', views.worktype_create, name='worktype_create'),  # URL для создания нового вида работ
    path('worktypes/edit/<int:pk>/', views.worktype_edit, name='worktype_edit'),  # URL для редактирования вида работ
    path('worktypes/delete/<int:pk>/', views.worktype_delete, name='worktype_delete'),  # URL для удаления вида работ


    path('worktypes/', views.worktype_list, name='worktype_list'),  # URL для отображения списка видов работ
    path('worktypes/create/', views.worktype_create, name='worktype_create'),  # URL для создания нового вида работ
    path('worktypes/edit/<int:pk>/', views.worktype_edit, name='worktype_edit'),  # URL для редактирования вида работ
    path('worktypes/delete/<int:pk>/', views.worktype_delete, name='worktype_delete'),  # URL для удаления вида работ
    path('worktypes/view/<int:pk>/', views.worktype_view, name='worktype_view'),  # URL для просмотра вида работ

   path('worktypes/export/', views.export_worktypes_to_excel, name='worktype_export'),


]
