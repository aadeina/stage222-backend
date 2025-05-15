from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    ChangePasswordView,
    LogoutView,
    VerifyEmailView,
    ResendEmailVerificationView,
    PasswordResetRequestView,
    PasswordResetView,
    GoogleLoginJWT, 
    FacebookCandidateLogin
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verification/', ResendEmailVerificationView.as_view(), name='resend-verification'),
    path('request-password-reset/', PasswordResetRequestView.as_view(), name='request-password-reset'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('social/google/', GoogleLoginJWT.as_view(), name='google-login'),
    path('social/facebook/', FacebookCandidateLogin.as_view(), name='facebook-login'),
]

