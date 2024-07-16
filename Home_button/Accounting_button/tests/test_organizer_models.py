from django.test import TestCase
from django.contrib.auth import get_user_model
from Accounting_button.models import OrganizerPositionDirectory, OrganizerTariff

User = get_user_model()

class OrganizerPositionDirectoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='password')
        self.position = OrganizerPositionDirectory.objects.create(
            position='Manager',
            comments='Responsible for managing the team',
            author=self.user
        )

    def test_position_creation(self):
        self.assertEqual(self.position.position, 'Manager')
        self.assertEqual(self.position.comments, 'Responsible for managing the team')
        self.assertEqual(self.position.author, self.user)
        self.assertEqual(self.position.author_name, self.user.get_full_name() or self.user.email)

    def test_position_str(self):
        self.assertEqual(str(self.position), 'Manager')

    def test_author_name_on_user_delete(self):
        self.user.delete()
        self.position.refresh_from_db()
        self.assertIsNone(self.position.author)
        self.assertEqual(self.position.author_name, 'testuser@example.com')  # или user.get_full_name(), если оно было установлено


class OrganizerTariffModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='password')
        self.position = OrganizerPositionDirectory.objects.create(
            position='Manager',
            comments='Responsible for managing the team',
            author=self.user
        )
        self.tariff = OrganizerTariff.objects.create(
            position=self.position,
            rate=0.5,
            base='Base description',
            author=self.user
        )

    def test_tariff_creation(self):
        self.assertEqual(self.tariff.position, self.position)
        self.assertEqual(self.tariff.rate, 0.5)
        self.assertEqual(self.tariff.base, 'Base description')
        self.assertEqual(self.tariff.author, self.user)
        self.assertEqual(self.tariff.author_name, self.user.get_full_name() or self.user.email)

    def test_tariff_str(self):
        self.assertEqual(str(self.tariff), 'Manager - 0.5')

    def test_author_name_on_user_delete(self):
        self.user.delete()
        self.tariff.refresh_from_db()
        self.assertIsNone(self.tariff.author)
        self.assertEqual(self.tariff.author_name, 'testuser@example.com')  # или user.get_full_name(), если оно было установлено
