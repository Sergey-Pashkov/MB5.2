from django.test import TestCase
from django.contrib.auth import get_user_model
from Accounting_button.models import Client, WorkTypeGroup, TariffDirectory, WorkType, StandardOperationsJournal, TaxSystem

class StandardOperationsJournalTest(TestCase):

    def setUp(self):
        # Создаем пользователя
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='password',
            first_name='Test',
            last_name='User',
            user_type='owner'
        )

        # Создаем систему налогообложения
        self.tax_system = TaxSystem.objects.create(
            name='Test Tax System'
        )

        # Создаем клиента
        self.client = Client.objects.create(
            short_name='Test Client',
            contract_price=1000.00,
            tax_system=self.tax_system  # Указываем значение для обязательного поля
        )

        # Создаем группу видов работ
        self.work_type_group = WorkTypeGroup.objects.create(
            name='Test Group',
            author=self.user
        )

        # Создаем тарифный справочник
        self.tariff_directory = TariffDirectory.objects.create(
            tariff_name='Test Tariff',
            cost_per_minute=1.5,
            author=self.user
        )

        # Создаем вид работы
        self.work_type = WorkType.objects.create(
            name='Test Work Type',
            time_norm=60,
            work_type_group=self.work_type_group,
            tariff_name=self.tariff_directory,
            author=self.user
        )

    def test_create_standard_operations_journal(self):
        # Создаем запись в журнале стандартных операций
        journal_entry = StandardOperationsJournal.objects.create(
            author=self.user,
            client=self.client,
            work_type=self.work_type,
            quantity=2
        )

        # Проверяем, что запись была создана
        self.assertEqual(StandardOperationsJournal.objects.count(), 1)

        # Проверяем значения полей
        self.assertEqual(journal_entry.author_name, self.user.get_full_name())
        self.assertEqual(journal_entry.client_display, f"{self.client.id} {self.client.short_name}")
        self.assertEqual(journal_entry.group, self.work_type.work_type_group.name)
        self.assertEqual(journal_entry.work_type_display, f"{self.work_type.id} {self.work_type.name}")
        self.assertEqual(journal_entry.time_norm, self.work_type.time_norm)
        self.assertEqual(journal_entry.tariff, self.work_type.tariff_cost)
        self.assertEqual(journal_entry.total_time, self.work_type.time_norm * 2)
        self.assertEqual(journal_entry.total_cost, self.work_type.tariff_cost * 2)
        self.assertIsNotNone(journal_entry.date)

    def test_str_method(self):
        # Создаем запись в журнале стандартных операций
        journal_entry = StandardOperationsJournal.objects.create(
            author=self.user,
            client=self.client,
            work_type=self.work_type,
            quantity=1
        )

        # Проверяем метод __str__
        expected_str = f"{journal_entry.author_name} - {journal_entry.client_display} - {journal_entry.work_type_display}"
        self.assertEqual(str(journal_entry), expected_str)
