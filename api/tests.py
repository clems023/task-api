from django.test import Client, TestCase
from rest_framework.test import APIClient


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


class TaskTests(TestCase):
    def setUp(self):
        self.client = APIClient()

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
