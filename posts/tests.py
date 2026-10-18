from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from .models import Post
from users.models import Follow


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


class PostFeedTests(APITestCase):
    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            email="feed@example.com",
            username="feeduser",
            password="StrongPass123",
        )
        self.followed_user = User.objects.create_user(
            email="followed@example.com",
            username="followed",
            password="StrongPass123",
        )
        self.other_user = User.objects.create_user(
            email="unfollowed@example.com",
            username="unfollowed",
            password="StrongPass123",
        )

        Follow.objects.create(
            follower=self.user,
            following=self.followed_user,
        )

        Post.objects.create(
            author=self.user,
            content="My own post",
        )
        Post.objects.create(
            author=self.followed_user,
            content="Post from followed user",
        )
        Post.objects.create(
            author=self.other_user,
            content="Post from unfollowed user",
        )

        token = Token.objects.create(user=self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token.key}"
        )

    def test_feed_contains_own_and_followed_posts(self):
        response = self.client.get("/api/posts/feed/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        contents = [
            post["content"] for post in response.data
        ]

        self.assertIn("My own post", contents)
        self.assertIn("Post from followed user", contents)
        self.assertNotIn("Post from unfollowed user", contents)
