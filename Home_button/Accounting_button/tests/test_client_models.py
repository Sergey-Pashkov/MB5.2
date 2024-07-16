# Accounting_button/tests/test_client_models.py

from django.test import TestCase
from Accounting_button.models import MyUser, TaxSystem, Client

class ClientModelTest(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create_user(
            email='testuser@example.com',
            password='password',
            first_name='Test',
            last_name='User'
        )
        self.tax_system = TaxSystem.objects.create(
            name='Test Tax System',
            author=self.user
        )
        self.client = Client.objects.create(
            short_name='Test Client',
            full_name='Test Client Full Name',
            contract_price=100000,
            contract_number_date='123/01-01-2024',
            inn='1234567890',
            tax_system=self.tax_system,
            activity_types='Consulting',
            contact_name='John Doe',
            phone_number='+123456789',
            email='client@example.com',
            postal_address='123 Main St',
            comment='Client Test comment',
            author=self.user
        )

    def test_client_creation(self):
        self.assertEqual(self.client.short_name, 'Test Client')
        self.assertEqual(self.client.full_name, 'Test Client Full Name')
        self.assertEqual(self.client.contract_price, 100000)
        self.assertEqual(self.client.contract_number_date, '123/01-01-2024')
        self.assertEqual(self.client.inn, '1234567890')
        self.assertEqual(self.client.tax_system, self.tax_system)
        self.assertEqual(self.client.activity_types, 'Consulting')
        self.assertEqual(self.client.contact_name, 'John Doe')
        self.assertEqual(self.client.phone_number, '+123456789')
        self.assertEqual(self.client.email, 'client@example.com')
        self.assertEqual(self.client.postal_address, '123 Main St')
        self.assertEqual(self.client.comment, 'Client Test comment')
        self.assertEqual(self.client.author, self.user)
        self.assertEqual(self.client.author_name, 'Test User')
        self.assertFalse(self.client.hide_in_list)

    def test_client_str(self):
        self.assertEqual(str(self.client), 'Test Client')

    def test_author_name_on_user_delete(self):
        self.user.delete()
        self.client.refresh_from_db()
        self.assertEqual(self.client.author_name, 'Test User')
        self.assertIsNone(self.client.author)
