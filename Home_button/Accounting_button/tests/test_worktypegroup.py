from django.test import TestCase
from django.contrib.auth import get_user_model
from Accounting_button.models import WorkTypeGroup

class WorkTypeGroupTest(TestCase):

    def setUp(self):
        # Создаем пользователя для тестов
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword123'
        )

    def test_create_worktypegroup(self):
        # Создаем экземпляр WorkTypeGroup
        group = WorkTypeGroup.objects.create(
            name='Test Group',
            comments='Test comments',
            author=self.user
        )
        
        # Проверяем, что группа была создана
        self.assertEqual(WorkTypeGroup.objects.count(), 1)
        
        # Проверяем, что автор был сохранен правильно
        self.assertEqual(group.author, self.user)
        self.assertEqual(group.author_name, self.user.get_full_name() or self.user.email)

    def test_history_creation(self):
        # Создаем экземпляр WorkTypeGroup
        group = WorkTypeGroup.objects.create(
            name='Test Group',
            comments='Test comments',
            author=self.user
        )

        # Проверяем, что история была создана
        self.assertEqual(group.history.all().count(), 1)

        # Обновляем группу
        group.name = 'Updated Group'
        group.save()

        # Проверяем, что запись в истории была добавлена
        self.assertEqual(group.history.all().count(), 2)
        self.assertEqual(group.history.first().name, 'Updated Group')
        self.assertEqual(group.history.last().name, 'Test Group')
