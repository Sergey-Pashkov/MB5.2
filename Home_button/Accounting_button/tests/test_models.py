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
