from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Accounting_button.views import (
    LoginView,
    DashboardRedirectView,
    OwnerDashboardView,
    OrganizerDashboardView,
    ExecutorDashboardView,
    OrganizerPositionDirectoryListView,
    OrganizerPositionDirectoryCreateView,
    OrganizerPositionDirectoryDetailView,
    OrganizerPositionDirectoryUpdateView,
    OrganizerPositionDirectoryDeleteView,
    OrganizerTariffListView,
    OrganizerTariffCreateView,
    OrganizerTariffDetailView,
    OrganizerTariffUpdateView,
    OrganizerTariffDeleteView
)

class TestUrls(SimpleTestCase):

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_dashboard_redirect_url(self):
        url = reverse('dashboard_redirect')
        self.assertEqual(resolve(url).func.view_class, DashboardRedirectView)

    def test_owner_dashboard_url(self):
        url = reverse('owner_dashboard')
        self.assertEqual(resolve(url).func.view_class, OwnerDashboardView)

    def test_organizer_dashboard_url(self):
        url = reverse('organizer_dashboard')
        self.assertEqual(resolve(url).func.view_class, OrganizerDashboardView)

    def test_executor_dashboard_url(self):
        url = reverse('executor_dashboard')
        self.assertEqual(resolve(url).func.view_class, ExecutorDashboardView)

    def test_positions_list_url_resolves(self):
        url = reverse('organizer_positions_list')
        self.assertEqual(resolve(url).func.view_class, OrganizerPositionDirectoryListView)

    def test_position_create_url_resolves(self):
        url = reverse('organizer_position_create')
        self.assertEqual(resolve(url).func.view_class, OrganizerPositionDirectoryCreateView)

    def test_position_detail_url_resolves(self):
        url = reverse('organizer_position_detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, OrganizerPositionDirectoryDetailView)

    def test_position_edit_url_resolves(self):
        url = reverse('organizer_position_edit', args=[1])
        self.assertEqual(resolve(url).func.view_class, OrganizerPositionDirectoryUpdateView)

    def test_position_delete_url_resolves(self):
        url = reverse('organizer_position_delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, OrganizerPositionDirectoryDeleteView)


    def test_organizer_tariffs_list_url(self):
        url = reverse('organizer_tariffs_list')
        self.assertEqual(resolve(url).func.view_class, OrganizerTariffListView)

    def test_organizer_tariff_create_url(self):
        url = reverse('organizer_tariff_create')
        self.assertEqual(resolve(url).func.view_class, OrganizerTariffCreateView)

    def test_organizer_tariff_detail_url(self):
        url = reverse('organizer_tariff_detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, OrganizerTariffDetailView)

    def test_organizer_tariff_edit_url(self):
        url = reverse('organizer_tariff_edit', args=[1])
        self.assertEqual(resolve(url).func.view_class, OrganizerTariffUpdateView)

    def test_organizer_tariff_delete_url(self):
        url = reverse('organizer_tariff_delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, OrganizerTariffDeleteView)
