from django.test import TestCase
from django.contrib.auth import get_user_model
from Accounting_button.models import TaxSystem

User = get_user_model()

class TaxSystemModelTest(TestCase):

    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='password'
        )

        # Создаем систему налогообложения
        self.tax_system = TaxSystem.objects.create(
            name='Упрощенная система налогообложения',
            comments='Комментарий к системе налогообложения',
            author=self.user
        )

    def test_tax_system_creation(self):
        # Проверяем, что система налогообложения создана корректно
        self.assertEqual(self.tax_system.name, 'Упрощенная система налогообложения')
        self.assertEqual(self.tax_system.comments, 'Комментарий к системе налогообложения')
        self.assertEqual(self.tax_system.author, self.user)
        self.assertEqual(self.tax_system.author_name, self.user.get_full_name() or self.user.email)

    def test_author_name_on_user_delete(self):
        # Удаляем автора
        self.user.delete()
        
        # Обновляем систему налогообложения из базы данных
        self.tax_system.refresh_from_db()

        # Проверяем, что имя автора сохранено, а поле author установлено в None
        self.assertIsNone(self.tax_system.author)
        self.assertEqual(self.tax_system.author_name, 'testuser@example.com')

    def test_tax_system_str(self):
        # Проверяем, что метод __str__ модели работает корректно
        self.assertEqual(str(self.tax_system), 'Упрощенная система налогообложения')
