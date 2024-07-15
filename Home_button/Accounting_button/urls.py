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
    OwnerDashboardView  
)


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
]
