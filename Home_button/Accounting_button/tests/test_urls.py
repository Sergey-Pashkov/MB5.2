# Accounting_button/tests/test_urls.py

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Accounting_button.views import LoginView, DashboardRedirectView, OwnerDashboardView, OrganizerDashboardView, ExecutorDashboardView

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
