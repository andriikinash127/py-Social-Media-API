from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from .models import Post


class PostPermissionTests(APITestCase):
    def test_unauthenticated_user_cannot_create_post(self):
        response = self.client.post(
            "/api/posts/",
            {"content": "Anonymous post"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.assertEqual(Post.objects.count(), 0)

    def test_user_cannot_update_another_users_post(self):
        User = get_user_model()

        author = User.objects.create_user(
            email="author@example.com",
            username="author",
            password="StrongPass123",
        )
        other_user = User.objects.create_user(
            email="other@example.com",
            username="other",
            password="StrongPass123",
        )

        post = Post.objects.create(
            author=author,
            content="Original content",
        )

        token = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.patch(
            f"/api/posts/{post.id}/",
            {"content": "Changed content"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        post.refresh_from_db()
        self.assertEqual(post.content, "Original content")
