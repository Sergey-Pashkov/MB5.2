from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class ExportClientsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpass'
        )
        self.client.login(email='testuser@example.com', password='testpass')

    def test_export_clients(self):
        response = self.client.get(reverse('export_clients'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.assertIn('attachment; filename=', response['Content-Disposition'])
