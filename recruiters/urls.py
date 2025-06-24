from django.urls import path
from .views import (
    RecruiterMeView,
    RecruiterDetailView,
    SendRecruiterOTPView,
    VerifyRecruiterOTPView,
    RecruiterOnboardingView,
)

urlpatterns = [
    path('me/', RecruiterMeView.as_view(), name='recruiter-me'),
    path('<uuid:user__id>/', RecruiterDetailView.as_view(), name='recruiter-detail'),
    path('onboarding/', RecruiterOnboardingView.as_view(), name='recruiter-onboarding'),

    # ✅ OTP verification endpoints
    path('send-otp/', SendRecruiterOTPView.as_view(), name='send-recruiter-otp'),
    path('verify-otp/', VerifyRecruiterOTPView.as_view(), name='verify-recruiter-otp'),
]