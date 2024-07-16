from django.test import TestCase
from django.contrib.auth import get_user_model
from Accounting_button.models import PositionDirectory, TariffDirectory

User = get_user_model()

class PositionDirectoryModelTest(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(email='testuser@example.com', password='password')
        # Создаем тестовую позицию
        self.position = PositionDirectory.objects.create(
            position='Manager',
            comments='Responsible for managing the team',
            author=self.user
        )

    def test_position_creation(self):
        # Проверяем создание позиции
        self.assertEqual(self.position.position, 'Manager')
        self.assertEqual(self.position.comments, 'Responsible for managing the team')
        self.assertEqual(self.position.author, self.user)
        self.assertEqual(self.position.author_name, self.user.get_full_name() or self.user.email)

    def test_position_str(self):
        # Проверяем строковое представление позиции
        self.assertEqual(str(self.position), 'Manager')

    def test_author_name_on_user_delete(self):
        # Проверяем сохранение имени автора после удаления пользователя
        self.user.delete()
        self.position.refresh_from_db()
        self.assertEqual(self.position.author, None)
        self.assertEqual(self.position.author_name, 'testuser@example.com')  # или user.get_full_name(), если оно было установлено


class TariffDirectoryModelTest(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(email='testuser@example.com', password='password')
        # Создаем тестовый тариф
        self.tariff = TariffDirectory.objects.create(
            tariff_name='Standard',
            cost_per_minute=0.50,
            comments='Standard tariff rate',
            author=self.user
        )

    def test_tariff_creation(self):
        # Проверяем создание тарифа
        self.assertEqual(self.tariff.tariff_name, 'Standard')
        self.assertEqual(self.tariff.cost_per_minute, 0.50)
        self.assertEqual(self.tariff.comments, 'Standard tariff rate')
        self.assertEqual(self.tariff.author, self.user)
        self.assertEqual(self.tariff.author_name, self.user.get_full_name() or self.user.email)

    def test_tariff_str(self):
        # Проверяем строковое представление тарифа
        self.assertEqual(str(self.tariff), 'Standard')

    def test_author_name_on_user_delete(self):
        # Проверяем сохранение имени автора после удаления пользователя
        self.user.delete()
        self.tariff.refresh_from_db()
        self.assertEqual(self.tariff.author, None)
        self.assertEqual(self.tariff.author_name, 'testuser@example.com')  # или user.get_full_name(), если оно было установлено
