from django.urls import path

from . import views

urlpatterns = [
    path(
        "/password/reset/<str:token>",
        views.PublicResetPassword.as_view(),
        name="user-reset-password",
    ),
    path(
        "/password/reset",
        views.PublicRequestPasswordReset.as_view(),
        name="user-request-password",
    ),
    path("/register", views.RegistrationAPIView.as_view(), name="register"),
    path("/login", views.LoginAPIView.as_view(), name="login"),
]
