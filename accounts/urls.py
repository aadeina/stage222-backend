from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    # Auth
    RegisterView,
    LoginView,
    LogoutView,
    ChangePasswordView,
    ProfileView,
    
    # Email verification
    VerifyEmailView,
    VerifyOTPView,
    ResendEmailVerificationView,
    ResendOTPVerificationView,
    

    # Password reset
    PasswordResetRequestView,
    PasswordResetView,

    # Social logins
    GoogleLoginJWT, 
    FacebookCandidateLogin,

)

urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Email Verification (OTP)
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),  # ✅ NEW
    path('resend-verification/', ResendEmailVerificationView.as_view(), name='resend-verification'),

    # Password Reset
    path('request-password-reset/', PasswordResetRequestView.as_view(), name='request-password-reset'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),

    # Social Logins
    path('social/google/', GoogleLoginJWT.as_view(), name='google-login'),
    path('social/facebook/', FacebookCandidateLogin.as_view(), name='facebook-login'),
    path('resend-otp/', ResendOTPVerificationView.as_view(), name='resend-otp'),


]
