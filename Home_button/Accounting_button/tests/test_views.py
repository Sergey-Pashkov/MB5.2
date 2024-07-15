# Accounting_button/tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from Accounting_button.models import MyUser, PositionDirectory, TariffDirectory, StaffSchedule

from django.test import TestCase, Client
from django.urls import reverse, resolve
from Accounting_button.models import MyUser
from Accounting_button.views import LoginView


class LoginViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = MyUser.objects.create_user(email='testuser@example.com', password='password')

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_login_form_valid(self):
        response = self.client.post(reverse('login'), {'username': 'testuser@example.com', 'password': 'password'})
        self.assertRedirects(response, reverse('dashboard_redirect'), status_code=302, target_status_code=200)



class DashboardRedirectViewTestCase(TestCase):
    def setUp(self):
        self.owner_user = MyUser.objects.create_user(email='owner@example.com', password='password', user_type='owner')
        self.organizer_user = MyUser.objects.create_user(email='organizer@example.com', password='password', user_type='organizer')
        self.executor_user = MyUser.objects.create_user(email='executor@example.com', password='password', user_type='executor')

    def test_owner_redirect(self):
        self.client.login(email='owner@example.com', password='password')
        response = self.client.get(reverse('dashboard_redirect'))
        self.assertRedirects(response, reverse('owner_dashboard'))

    def test_organizer_redirect(self):
        self.client.login(email='organizer@example.com', password='password')
        response = self.client.get(reverse('dashboard_redirect'))
        self.assertRedirects(response, reverse('organizer_dashboard'))

    def test_executor_redirect(self):
        self.client.login(email='executor@example.com', password='password')
        response = self.client.get(reverse('dashboard_redirect'))
        self.assertRedirects(response, reverse('executor_dashboard'))

class StaffScheduleViewTestCase(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(email='testuser@example.com', password='testpassword', user_type='owner')
        self.client.login(email='testuser@example.com', password='testpassword')
        self.position = PositionDirectory.objects.create(position='Manager')
        self.tariff = TariffDirectory.objects.create(tariff_name='Standard', cost_per_minute=1.00)
        self.schedule = StaffSchedule.objects.create(
            user=self.user,
            position=self.position,
            tariff=self.tariff,
            quantity=2,
            norm_time_per_month=160
        )

    def test_staff_schedule_list_view(self):
        response = self.client.get(reverse('staff_schedule_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounting_button/staff_schedule_list.html')

    def test_staff_schedule_detail_view(self):
        response = self.client.get(reverse('staff_schedule_detail', args=[self.schedule.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounting_button/staff_schedule_detail.html')

    def test_staff_schedule_create_view(self):
        response = self.client.post(reverse('staff_schedule_create'), {
            'position': self.position.id,
            'tariff': self.tariff.id,
            'quantity': 2,
            'norm_time_per_month': 160,
        })
        self.assertEqual(response.status_code, 302)  # Redirection status code
        self.assertEqual(StaffSchedule.objects.count(), 2)  # Expecting 2 objects now

    def test_staff_schedule_update_view(self):
        response = self.client.post(reverse('staff_schedule_edit', args=[self.schedule.id]), {
            'position': self.position.id,
            'tariff': self.tariff.id,
            'quantity': 4,
            'norm_time_per_month': 160,
        })
        self.schedule.refresh_from_db()
        self.assertEqual(self.schedule.quantity, 4)  # Expecting updated quantity to be 4

    def test_staff_schedule_delete_view(self):
        response = self.client.post(reverse('staff_schedule_delete', args=[self.schedule.id]))
        self.assertEqual(response.status_code, 302)  # Redirection status code
        self.assertEqual(StaffSchedule.objects.count(), 0)  # Expecting 0 objects now
