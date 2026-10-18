from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from users.models import Follow

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


class UserLogoutTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="logout@example.com",
            username="logoutuser",
            password="StrongPass123",
        )
        self.token = Token.objects.create(user=self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

    def test_logout_deletes_token(self):
        response = self.client.post("/api/users/logout/")

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Token.objects.filter(user=self.user).exists()
        )

    def test_login_with_wrong_password(self):
        response = self.client.post(
            "/api/users/login/",
            {
                "email": "login@example.com",
                "password": "WrongPassword123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertNotIn("token", response.data)


class UserFollowTests(APITestCase):
    def setUp(self):
        self.follower = User.objects.create_user(
            email="follower@example.com",
            username="follower",
            password="StrongPass123",
        )
        self.following = User.objects.create_user(
            email="following@example.com",
            username="following",
            password="StrongPass123",
        )

        self.token = Token.objects.create(user=self.follower)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

    def test_user_can_follow_another_user(self):
        response = self.client.post(
            "/api/users/follow/following/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertTrue(
            Follow.objects.filter(
                follower=self.follower,
                following=self.following,
            ).exists()
        )

    def test_cannot_follow_same_user_twice(self):
        Follow.objects.create(
            follower=self.follower,
            following=self.following,
        )

        response = self.client.post(
            "/api/users/follow/following/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(Follow.objects.count(), 1)

    def test_cannot_follow_self(self):
        response = self.client.post(
            f"/api/users/follow/{self.follower.username}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertFalse(
            Follow.objects.filter(
                follower=self.follower,
                following=self.follower,
            ).exists()
        )
