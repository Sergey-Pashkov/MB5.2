from django.test import TestCase, Client as TestClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from Accounting_button.models import Client as ClientModel, TaxSystem

class ClientViewTests(TestCase):

    def setUp(self):
        self.client = TestClient()
        self.user_owner = get_user_model().objects.create_user(email='owner@example.com', password='password', user_type='owner')
        self.user_organizer = get_user_model().objects.create_user(email='organizer@example.com', password='password', user_type='organizer')
        self.user_executor = get_user_model().objects.create_user(email='executor@example.com', password='password', user_type='executor')
        self.tax_system = TaxSystem.objects.create(name='Tax System')

        self.client_1 = ClientModel.objects.create(
            short_name='Client 1',
            full_name='Full Name 1',
            contract_price=1000,
            contract_number_date='1234',
            inn='123456789012',
            tax_system=self.tax_system,
            nomenclature_units=10,
            activity_types='Activity 1',
            contact_name='Contact 1',
            phone_number='1234567890',
            email='client1@example.com',
            postal_address='Address 1',
            comment='Comment 1',
            author=self.user_owner
        )

    def test_client_list_owner(self):
        self.client.login(email='owner@example.com', password='password')
        response = self.client.get(reverse('client_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Client 1')

    def test_client_list_organizer(self):
        self.client.login(email='organizer@example.com', password='password')
        response = self.client.get(reverse('client_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Client 1')

    def test_client_list_executor(self):
        self.client.login(email='executor@example.com', password='password')
        response = self.client.get(reverse('client_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Client 1')

    def test_client_create_view_owner(self):
        self.client.login(email='owner@example.com', password='password')
        response = self.client.get(reverse('client_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounting_button/Client_list/client_form.html')

    def test_client_update_view_organizer(self):
        self.client.login(email='organizer@example.com', password='password')
        response = self.client.get(reverse('client_edit', kwargs={'pk': self.client_1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounting_button/Client_list/client_form.html')

    def test_client_update_view_executor(self):
        self.client.login(email='executor@example.com', password='password')
        response = self.client.get(reverse('client_edit', kwargs={'pk': self.client_1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounting_button/Client_list/client_form.html')

    def test_client_delete_view_owner(self):
        self.client.login(email='owner@example.com', password='password')
        response = self.client.get(reverse('client_delete', kwargs={'pk': self.client_1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounting_button/Client_list/client_confirm_delete.html')

    def test_client_delete_view_organizer(self):
        self.client.login(email='organizer@example.com', password='password')
        response = self.client.get(reverse('client_delete', kwargs={'pk': self.client_1.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect to forbidden

    def test_client_delete_view_executor(self):
        self.client.login(email='executor@example.com', password='password')
        response = self.client.get(reverse('client_delete', kwargs={'pk': self.client_1.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect to forbidden
