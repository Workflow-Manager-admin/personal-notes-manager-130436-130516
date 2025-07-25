from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User

class HealthTests(APITestCase):
    def test_health(self):
        url = reverse('Health')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "Server is up!"})

class AuthTests(APITestCase):
    def test_register_login_logout(self):
        # Register
        reg_url = reverse('register')
        payload = {"username": "tester", "password": "testpass123", "email": "test@example.com"}
        response = self.client.post(reg_url, payload)
        self.assertEqual(response.status_code, 201)
        # Login
        login_url = reverse('login')
        response = self.client.post(login_url, {"username": "tester", "password": "testpass123"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.data)
        # Set session for authenticated requests
        self.client.login(username="tester", password="testpass123")
        # Logout
        logout_url = reverse('logout')
        response = self.client.post(logout_url)
        self.assertEqual(response.status_code, 200)

class NoteApiTests(APITestCase):
    def setUp(self):
        # Create user and log in
        self.user = User.objects.create_user(username="nuser", password="npassw123")
        self.client.login(username="nuser", password="npassw123")

    def test_note_crud_and_search(self):
        # Create note
        url = reverse('note-list-create')
        payload = {"title": "Buy milk", "content": "Remember to buy milk at the store."}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 201)
        note_id = response.data["id"]
        # List notes and check filtering by owner
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Buy milk")
        # Search note
        response = self.client.get(url, {"search": "milk"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(url, {"search": "other"})
        self.assertEqual(len(response.data), 0)
        # Get detail
        detail_url = reverse('note-detail', kwargs={"note_id": note_id})
        response = self.client.get(detail_url)
        self.assertEqual(response.data["title"], "Buy milk")
        # Update note
        response = self.client.put(detail_url, {"title": "Buy bread", "content": "Whole wheat", "owner": self.user.username})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Buy bread")
        # Delete note
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, 204)
        # Ensure note deleted
        response = self.client.get(url)
        self.assertEqual(len(response.data), 0)
