from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter

from .models import Profile, Follow
from .serializers import (
    UserLoginSerializer,
    UserRegistrationSerializer,
    ProfileSerializer,
    UserSearchSerializer,
)


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {"token": token.key},
            status=status.HTTP_200_OK,
        )


class UserLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={
            204: OpenApiResponse(description="Logged out successfully."),
        },
    )
    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile


class PublicProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user = get_object_or_404(
            get_user_model(),
            username=self.kwargs["username"],
        )
        profile, _ = Profile.objects.get_or_create(user=user)
        return profile


class UserSearchView(generics.ListAPIView):
    serializer_class = UserSearchSerializer
    permission_classes = [AllowAny]
    queryset = get_user_model().objects.all()
    filter_backends = [SearchFilter]
    search_fields = ["username"]


class FollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={
            201: OpenApiResponse(description="Followed successfully."),
            200: OpenApiResponse(description="Already following this user."),
            400: OpenApiResponse(description="Cannot follow yourself."),
            404: OpenApiResponse(description="User not found."),
        },
    )
    def post(self, request, username):
        target_user = get_object_or_404(
            get_user_model(),
            username=username,
        )

        if target_user == request.user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        _, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target_user,
        )

        if not created:
            return Response(
                {"detail": "Already following this user."},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"detail": "Followed successfully."},
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        request=None,
        responses={
            204: OpenApiResponse(description="Unfollowed successfully."),
            404: OpenApiResponse(description="User not found."),
        },
    )
    def delete(self, request, username):
        target_user = get_object_or_404(
            get_user_model(),
            username=username,
        )

        Follow.objects.filter(
            follower=request.user,
            following=target_user,
        ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowingListView(generics.ListAPIView):
    serializer_class = UserSearchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            get_user_model()
            .objects.filter(follower_relations__follower=self.request.user)
            .distinct()
            .order_by("username")
        )


class FollowersListView(generics.ListAPIView):
    serializer_class = UserSearchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            get_user_model()
            .objects.filter(following_relations__following=self.request.user)
            .distinct()
            .order_by("username")
        )
