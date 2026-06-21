from django.contrib.auth.models import User
from django.test import Client, TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Task


class HomeTests(TestCase):
    def test_homepage_returns_200(self):
        response = Client().get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task API")


class HealthTests(TestCase):
    def test_health_returns_ok(self):
        response = APIClient().get("/api/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})


class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "alice",
                "email": "alice@example.com",
                "password": "securepass123",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["username"], "alice")
        self.assertTrue(User.objects.filter(username="alice").exists())

    def test_obtain_token(self):
        User.objects.create_user(username="bob", password="securepass123")
        response = self.client.post(
            "/api/auth/token/",
            {"username": "bob", "password": "securepass123"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())

    def test_tasks_require_authentication(self):
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TaskTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.other = User.objects.create_user(username="other", password="testpass123")
        self.client = APIClient()
        token_response = self.client.post(
            "/api/auth/token/",
            {"username": "testuser", "password": "testpass123"},
            format="json",
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token_response.json()['access']}"
        )

    def test_create_task(self):
        response = self.client.post(
            "/api/tasks/",
            {"title": "Ma première tâche"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Ma première tâche")
        self.assertFalse(response.json()["done"])

    def test_list_tasks(self):
        self.client.post(
            "/api/tasks/",
            {"title": "Tâche test"},
            format="json",
        )
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)

    def test_user_only_sees_own_tasks(self):
        Task.objects.create(user=self.other, title="Tâche autre")
        self.client.post("/api/tasks/", {"title": "Ma tâche"}, format="json")

        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["title"], "Ma tâche")
