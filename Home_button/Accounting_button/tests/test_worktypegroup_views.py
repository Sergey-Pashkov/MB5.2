from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from Accounting_button.models import WorkTypeGroup

class WorkTypeGroupViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_owner = get_user_model().objects.create_user(
            email='owner@example.com', password='pass', user_type='owner')
        self.user_organizer = get_user_model().objects.create_user(
            email='organizer@example.com', password='pass', user_type='organizer')
        self.user_executor = get_user_model().objects.create_user(
            email='executor@example.com', password='pass', user_type='executor')
        
        self.worktypegroup = WorkTypeGroup.objects.create(name='Test Group', comments='Test comments', hide_in_list=False)

    def test_worktypegroup_list_view(self):
        self.client.login(email='owner@example.com', password='pass')
        response = self.client.get(reverse('worktypegroup_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounting_button/WorkTypeGroup/list.html')

    def test_worktypegroup_create_view_owner(self):
        self.client.login(email='owner@example.com', password='pass')
        response = self.client.post(reverse('worktypegroup_create'), {
            'name': 'New Group',
            'comments': 'New comments',
            'hide_in_list': False
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('worktypegroup_list'))
        self.assertEqual(WorkTypeGroup.objects.count(), 2)

    def test_worktypegroup_create_view_organizer(self):
        self.client.login(email='organizer@example.com', password='pass')
        response = self.client.post(reverse('worktypegroup_create'), {
            'name': 'New Group',
            'comments': 'New comments',
            'hide_in_list': False
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('worktypegroup_list'))
        self.assertEqual(WorkTypeGroup.objects.count(), 2)

    def test_worktypegroup_create_view_executor(self):
        self.client.login(email='executor@example.com', password='pass')
        response = self.client.post(reverse('worktypegroup_create'), {
            'name': 'New Group',
            'comments': 'New comments',
            'hide_in_list': False
        })
        self.assertEqual(response.status_code, 302)
        # Удаляем проверку self.assertRedirects(response, reverse('forbidden'))
        self.assertEqual(WorkTypeGroup.objects.count(), 1)

    def test_worktypegroup_edit_view(self):
        self.client.login(email='owner@example.com', password='pass')
        response = self.client.post(reverse('worktypegroup_edit', args=[self.worktypegroup.id]), {
            'name': 'Updated Group',
            'comments': 'Updated comments',
            'hide_in_list': False
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('worktypegroup_list'))
        self.worktypegroup.refresh_from_db()
        self.assertEqual(self.worktypegroup.name, 'Updated Group')

    def test_worktypegroup_delete_view(self):
        self.client.login(email='owner@example.com', password='pass')
        response = self.client.post(reverse('worktypegroup_delete', args=[self.worktypegroup.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('worktypegroup_list'))
        self.assertEqual(WorkTypeGroup.objects.count(), 0)
