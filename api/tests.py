from django.contrib.auth.models import User
from django.test import Client, TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Task


class AuthenticatedAPITestCase(TestCase):
    """Client API authentifié avec JWT pour l'utilisateur testuser."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.other = User.objects.create_user(
            username="other", password="testpass123"
        )
        self.client = APIClient()
        token_response = self.client.post(
            "/api/auth/token/",
            {"username": "testuser", "password": "testpass123"},
            format="json",
        )
        self.access_token = token_response.json()["access"]
        self.refresh_token = token_response.json()["refresh"]
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

    def create_task(self, title="Tâche test", done=False, user=None):
        return Task.objects.create(
            user=user or self.user,
            title=title,
            done=done,
        )


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


class RegisterTests(TestCase):
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["username"], "alice")
        self.assertTrue(User.objects.filter(username="alice").exists())

    def test_register_rejects_short_password(self):
        response = self.client.post(
            "/api/auth/register/",
            {"username": "alice", "password": "short"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TokenTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        User.objects.create_user(username="bob", password="securepass123")

    def test_obtain_token(self):
        response = self.client.post(
            "/api/auth/token/",
            {"username": "bob", "password": "securepass123"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())

    def test_obtain_token_invalid_credentials(self):
        response = self.client.post(
            "/api/auth/token/",
            {"username": "bob", "password": "wrongpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token(self):
        token_response = self.client.post(
            "/api/auth/token/",
            {"username": "bob", "password": "securepass123"},
            format="json",
        )
        response = self.client.post(
            "/api/auth/token/refresh/",
            {"refresh": token_response.json()["refresh"]},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.json())

    def test_refresh_token_invalid(self):
        response = self.client.post(
            "/api/auth/token/refresh/",
            {"refresh": "invalid-token"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TaskAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_tasks_requires_authentication(self):
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_task_requires_authentication(self):
        response = self.client.post(
            "/api/tasks/",
            {"title": "Sans auth"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_task_requires_authentication(self):
        user = User.objects.create_user(username="u", password="testpass123")
        task = Task.objects.create(user=user, title="Tâche")
        response = self.client.get(f"/api/tasks/{task.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_task_requires_authentication(self):
        user = User.objects.create_user(username="u", password="testpass123")
        task = Task.objects.create(user=user, title="Tâche")
        response = self.client.patch(
            f"/api/tasks/{task.id}/",
            {"done": True},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_task_requires_authentication(self):
        user = User.objects.create_user(username="u", password="testpass123")
        task = Task.objects.create(user=user, title="Tâche")
        response = self.client.delete(f"/api/tasks/{task.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TaskCRUDTests(AuthenticatedAPITestCase):
    def test_create_task(self):
        response = self.client.post(
            "/api/tasks/",
            {"title": "Ma première tâche"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], "Ma première tâche")
        self.assertFalse(response.json()["done"])

    def test_list_tasks(self):
        self.create_task(title="Tâche test")
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)

    def test_retrieve_task(self):
        task = self.create_task(title="Détail tâche")
        response = self.client.get(f"/api/tasks/{task.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Détail tâche")

    def test_patch_task(self):
        task = self.create_task(title="À modifier")
        response = self.client.patch(
            f"/api/tasks/{task.id}/",
            {"done": True},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["done"])
        task.refresh_from_db()
        self.assertTrue(task.done)

    def test_delete_task(self):
        task = self.create_task(title="À supprimer")
        response = self.client.delete(f"/api/tasks/{task.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_user_only_sees_own_tasks(self):
        self.create_task(title="Ma tâche")
        Task.objects.create(user=self.other, title="Tâche autre")

        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["title"], "Ma tâche")

    def test_cannot_retrieve_other_user_task(self):
        other_task = Task.objects.create(user=self.other, title="Tâche autre")
        response = self.client.get(f"/api/tasks/{other_task.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_patch_other_user_task(self):
        other_task = Task.objects.create(user=self.other, title="Tâche autre")
        response = self.client.patch(
            f"/api/tasks/{other_task.id}/",
            {"done": True},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_delete_other_user_task(self):
        other_task = Task.objects.create(user=self.other, title="Tâche autre")
        response = self.client.delete(f"/api/tasks/{other_task.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
