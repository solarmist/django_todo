from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Task


class TaskModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="testuser", password="password")
        Task.objects.create(title="Test Task", user=user)

    def test_task_creation(self):
        task = Task.objects.get(title="Test Task")
        self.assertEqual(task.title, "Test Task")
