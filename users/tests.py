from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserRegistrationTests(APITestCase):
    def test_register_user(self):
        payload = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "StrongPass123",
        }

        response = self.client.post(
            "/api/users/register/",
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertNotIn("password", response.data)
        self.assertTrue(User.objects.filter(email=payload["email"]).exists())

        user = User.objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))


class UserLoginTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="login@example.com",
            username="loginuser",
            password="StrongPass123",
        )

    def test_login_returns_token(self):
        response = self.client.post(
            "/api/users/login/",
            {
                "email": "login@example.com",
                "password": "StrongPass123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertIn("token", response.data)
        self.assertTrue(response.data["token"])
