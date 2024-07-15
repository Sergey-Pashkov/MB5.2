from django.test import TestCase, Client
from django.urls import reverse
from Accounting_button.models import TaxSystem, MyUser as User

class TaxSystemViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='owner@example.com',
            password='password',
            user_type='owner'
        )
        self.client.login(email='owner@example.com', password='password')

        self.tax_system = TaxSystem.objects.create(
            name='Упрощенная система налогообложения',
            comments='Комментарий к системе налогообложения',
            author=self.user
        )

    def test_tax_system_list_view(self):
        response = self.client.get(reverse('tax_system_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Упрощенная система налогообложения')
        self.assertTemplateUsed(response, 'Accounting_button/tax_system/tax_system_list.html')

    def test_tax_system_detail_view(self):
        response = self.client.get(reverse('tax_system_detail', args=[self.tax_system.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Упрощенная система налогообложения')
        self.assertTemplateUsed(response, 'Accounting_button/tax_system/tax_system_detail.html')

    def test_tax_system_create_view(self):
        response = self.client.post(reverse('tax_system_create'), {
            'name': 'Основная система налогообложения',
            'comments': 'Комментарий к основной системе',
            'author': self.user.pk
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(TaxSystem.objects.filter(name='Основная система налогообложения').exists())

    def test_tax_system_update_view(self):
        response = self.client.post(reverse('tax_system_edit', args=[self.tax_system.pk]), {
            'name': 'Обновленная система налогообложения',
            'comments': 'Обновленный комментарий',
            'author': self.user.pk
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.tax_system.refresh_from_db()
        self.assertEqual(self.tax_system.name, 'Обновленная система налогообложения')

    def test_tax_system_delete_view(self):
        response = self.client.post(reverse('tax_system_delete', args=[self.tax_system.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful delete
        self.assertFalse(TaxSystem.objects.filter(pk=self.tax_system.pk).exists())
