# myapp/tests/test_models.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import StaffSchedule, TariffDirectory, PositionDirectory, MyUser




class MyUserTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='password',
            first_name='Test',
            last_name='User',
            user_type='owner'
        )

    def test_create_user(self):
        user = get_user_model().objects.get(email='testuser@example.com')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('password'))
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.user_type, 'owner')

class TariffDirectoryTestCase(TestCase):
    def setUp(self):
        TariffDirectory.objects.create(tariff_name="Standard", cost_per_minute=2.5)
        TariffDirectory.objects.create(tariff_name="Premium", cost_per_minute=5.0)

    def test_tariff_directory_str(self):
        standard_tariff = TariffDirectory.objects.get(tariff_name="Standard")
        premium_tariff = TariffDirectory.objects.get(tariff_name="Premium")
        self.assertEqual(str(standard_tariff), "Standard")
        self.assertEqual(str(premium_tariff), "Premium")

class PositionDirectoryTestCase(TestCase):
    def setUp(self):
        PositionDirectory.objects.create(position="Developer")
        PositionDirectory.objects.create(position="Manager")

    def test_position_directory_str(self):
        developer_position = PositionDirectory.objects.get(position="Developer")
        manager_position = PositionDirectory.objects.get(position="Manager")
        self.assertEqual(str(developer_position), "Developer")
        self.assertEqual(str(manager_position), "Manager")

class StaffScheduleTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='testuser@example.com', password='password')
        self.position = PositionDirectory.objects.create(position='Developer')
        self.tariff = TariffDirectory.objects.create(tariff_name='Standard', cost_per_minute=1.5)
        self.schedule = StaffSchedule.objects.create(
            user=self.user,
            position=self.position,
            tariff=self.tariff,
            quantity=2,
            norm_time_per_month=160
        )

    def test_total_working_time(self):
        self.assertEqual(self.schedule.total_working_time, 320)  # 2 * 160

    def test_total_salary_fund(self):
        self.assertEqual(self.schedule.total_salary_fund, 480.0)  # 320 * 1.5

    def test_staff_schedule_str(self):
        self.assertEqual(str(self.schedule), "Developer - 2")

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import OrganizerPositionDirectory
from Accounting_button.models import OrganizerPositionDirectory, MyUser  # Импортируйте вашу пользовательскую модель


class OrganizerPositionDirectoryTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.owner = MyUser.objects.create_user(email='owner@example.com', password='password', user_type='owner')  # Используйте вашу пользовательскую модель
        self.client.login(username='owner@example.com', password='password')
        
        self.position = OrganizerPositionDirectory.objects.create(position="Test Position", comments="Test comments")
    
    def test_positions_list_view(self):
        response = self.client.get(reverse('organizer_positions_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Position")
    
    def test_position_detail_view(self):
        response = self.client.get(reverse('organizer_position_detail', args=[self.position.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Position")
        self.assertContains(response, "Test comments")
    
    def test_position_create_view(self):
        response = self.client.post(reverse('organizer_position_create'), {
            'position': 'New Position',
            'comments': 'New comments'
        })
        self.assertEqual(response.status_code, 302)  # Проверяем, что редирект произошел
        new_position = OrganizerPositionDirectory.objects.get(position='New Position')
        self.assertEqual(new_position.comments, 'New comments')
    
    def test_position_update_view(self):
        response = self.client.post(reverse('organizer_position_edit', args=[self.position.id]), {
            'position': 'Updated Position',
            'comments': 'Updated comments'
        })
        self.assertEqual(response.status_code, 302)  # Проверяем, что редирект произошел
        self.position.refresh_from_db()
        self.assertEqual(self.position.position, 'Updated Position')
        self.assertEqual(self.position.comments, 'Updated comments')
    
    def test_position_delete_view(self):
        response = self.client.post(reverse('organizer_position_delete', args=[self.position.id]))
        self.assertEqual(response.status_code, 302)  # Проверяем, что редирект произошел
        with self.assertRaises(OrganizerPositionDirectory.DoesNotExist):
            OrganizerPositionDirectory.objects.get(id=self.position.id)


class OrganizerPositionDirectoryModelTests(TestCase):

    def setUp(self):
        self.position = OrganizerPositionDirectory.objects.create(
            position="Test Position",
            comments="Test comments"
        )

    def test_position_creation(self):
        self.assertEqual(self.position.position, "Test Position")
        self.assertEqual(self.position.comments, "Test comments")


from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from Accounting_button.models import OrganizerTariff, OrganizerPositionDirectory

User = get_user_model()

class OrganizerTariffViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(email='owner@example.com', password='password', user_type='owner')
        self.organizer = User.objects.create_user(email='organizer@example.com', password='password', user_type='organizer')
        self.position = OrganizerPositionDirectory.objects.create(position='Organizer Position')
        self.tariff = OrganizerTariff.objects.create(position=self.position, rate=0.5, base='Base info')

    def test_organizer_tariff_list_view(self):
        self.client.login(email='owner@example.com', password='password')
        response = self.client.get(reverse('organizer_tariffs_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounting_button/organizer_tariffs/organizer_tariff_list.html')

    def test_organizer_tariff_detail_view(self):
        self.client.login(email='owner@example.com', password='password')
        response = self.client.get(reverse('organizer_tariff_detail', args=[self.tariff.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounting_button/organizer_tariffs/organizer_tariff_detail.html')

    def test_organizer_tariff_create_view(self):
        self.client.login(email='owner@example.com', password='password')
        response = self.client.get(reverse('organizer_tariff_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounting_button/organizer_tariffs/organizer_tariff_form.html')
        response = self.client.post(reverse('organizer_tariff_create'), {
            'position': self.position.id,
            'rate': 0.8,
            'base': 'New Base Info'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation

    def test_organizer_tariff_update_view(self):
        self.client.login(email='owner@example.com', password='password')
        response = self.client.get(reverse('organizer_tariff_edit', args=[self.tariff.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounting_button/organizer_tariffs/organizer_tariff_form.html')
        response = self.client.post(reverse('organizer_tariff_edit', args=[self.tariff.id]), {
            'position': self.position.id,
            'rate': 0.9,
            'base': 'Updated Base Info'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update

    def test_organizer_tariff_delete_view(self):
        self.client.login(email='owner@example.com', password='password')
        response = self.client.get(reverse('organizer_tariff_delete', args=[self.tariff.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounting_button/organizer_tariffs/organizer_tariff_confirm_delete.html')
        response = self.client.post(reverse('organizer_tariff_delete', args=[self.tariff.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
