from django.urls import path

from .views import (
    UserLoginView,
    UserRegistrationView,
    UserLogoutView,
    ProfileView,
    PublicProfileView,
    UserSearchView,
)

urlpatterns = [
    path(
        "register/",
        UserRegistrationView.as_view(),
        name="user-register",
    ),
    path(
        "login/",
        UserLoginView.as_view(),
        name="user-login",
    ),
    path(
        "logout/",
        UserLogoutView.as_view(),
        name="user-logout",
    ),
    path(
        "me/",
        ProfileView.as_view(),
        name="my-profile",
    ),
    path(
        "profiles/<str:username>/",
        PublicProfileView.as_view(),
        name="public-profile",
    ),
    path(
        "search/",
        UserSearchView.as_view(),
        name="user-search",
    ),
]
