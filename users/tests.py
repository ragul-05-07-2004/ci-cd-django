from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class RegisterTest(APITestCase):

    def test_register_user(self):
        data = {
            "username": "john",
            "email": "john@gmail.com",
            "password": "Password123",
        }

        response = self.client.post("/api/users/register/", data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "User registered successfully")

        self.assertTrue(User.objects.filter(username="john").exists())

    def test_register_duplicate_username(self):
        User.objects.create_user(
            username="john", email="old@gmail.com", password="Password123"
        )

        data = {
            "username": "john",
            "email": "new@gmail.com",
            "password": "Password123",
        }

        response = self.client.post("/api/users/register/", data, format="json")

        self.assertEqual(response.status_code, 400)


class LoginTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="john", email="john@gmail.com", password="Password123"
        )

    def test_login_success(self):
        data = {
            "username": "john",
            "password": "Password123",
        }

        response = self.client.post("/api/users/login/", data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Login successful")

    def test_login_wrong_password(self):
        data = {
            "username": "john",
            "password": "WrongPassword",
        }

        response = self.client.post("/api/users/login/", data, format="json")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["message"], "Invalid username or password")
