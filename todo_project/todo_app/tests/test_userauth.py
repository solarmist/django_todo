from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class UserAuthTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registration(self):
        response = self.client.post(
            reverse("register"),
            {
                "email": "newuser@place.com",
                "username": "newuser",
                "password1": "complexpassword123",
                "password2": "complexpassword123",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect after registration
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login(self):
        User.objects.create_user(username="testuser", password="password")
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "password"}
        )
        self.assertEqual(response.status_code, 302)  # Redirect after login

    def test_logout(self):
        User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)  # Redirect after logout
