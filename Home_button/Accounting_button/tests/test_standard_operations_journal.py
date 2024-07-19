from django.test import TestCase
from django.core.exceptions import ValidationError
from Accounting_button.models import (
    StandardOperationsJournal, Client, WorkType, WorkTypeGroup, 
    TariffDirectory, TaxSystem
)
from django.contrib.auth import get_user_model

class StandardOperationsJournalTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com', password='testpassword'
        )
        self.tax_system = TaxSystem.objects.create(
            name="Test Tax System"
        )
        self.client = Client.objects.create(
            short_name="Test Client",
            contract_price=1000,
            tax_system=self.tax_system
        )
        self.work_type_group = WorkTypeGroup.objects.create(
            name='Test Group'
        )
        self.tariff_directory = TariffDirectory.objects.create(
            tariff_name='Standard Tariff',
            cost_per_minute=10.00
        )
        self.work_type = WorkType.objects.create(
            name='Test WorkType',
            time_norm=30,
            work_type_group=self.work_type_group,
            tariff_name=self.tariff_directory
        )

    def test_create_standard_operations_journal(self):
        journal_entry = StandardOperationsJournal.objects.create(
            author=self.user,
            client=self.client,
            work_type=self.work_type,
            quantity=2
        )
        self.assertEqual(journal_entry.total_time, 60)
        self.assertEqual(journal_entry.total_cost, 20.00)

    def test_str_method(self):
        journal_entry = StandardOperationsJournal.objects.create(
            author=self.user,
            client=self.client,
            work_type=self.work_type,
            quantity=2
        )
        expected_str = f"{self.user.get_full_name()} - {self.client.id} {self.client.short_name} - {self.work_type.id} {self.work_type.name}"
        self.assertEqual(str(journal_entry), expected_str)

    def test_negative_quantity(self):
        journal_entry = StandardOperationsJournal.objects.create(
            author=self.user,
            client=self.client,
            work_type=self.work_type,
            quantity=-1
        )
        self.assertEqual(journal_entry.total_time, -30)
        self.assertEqual(journal_entry.total_cost, -10.00)

    def test_zero_quantity_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            StandardOperationsJournal.objects.create(
                author=self.user,
                client=self.client,
                work_type=self.work_type,
                quantity=0
            )
