from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from ..models import Task


class TaskViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

    def test_task_list_view(self):
        response = self.client.get(reverse("task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_list.html")

    def test_add_task_view(self):
        response = self.client.post(reverse("add-task"), {"title": "New Task Title"})
        self.assertEqual(response.status_code, 302)  # Redirect after adding task
        self.assertEqual(Task.objects.count(), 1)

    def test_mark_as_done(self):
        task = Task.objects.create(title="Incomplete Task", user=self.user)
        response = self.client.post(
            reverse("mark-as-done", args=[task.id]), {"completed": "true"}
        )
        task.refresh_from_db()
        self.assertIsNotNone(task.completed_on)

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get(reverse("task-list"))
        self.assertRedirects(response, "/login?next=/")
