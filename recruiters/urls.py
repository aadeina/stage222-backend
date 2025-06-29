from django.urls import path
from .views import (
    RecruiterMeView,
    RecruiterDetailView,
    SendRecruiterOTPView,
    VerifyRecruiterOTPView,
    RecruiterOnboardingView,
    RecruiterDashboardOpportunitiesView,
    RecruiterDashboardStatsView,
)




urlpatterns = [
    path('me/', RecruiterMeView.as_view(), name='recruiter-me'),
    path('<uuid:user__id>/', RecruiterDetailView.as_view(), name='recruiter-detail'),
    path('onboarding/', RecruiterOnboardingView.as_view(), name='recruiter-onboarding'),

    # ✅ OTP verification endpoints
    path('send-otp/', SendRecruiterOTPView.as_view(), name='send-recruiter-otp'),
    path('verify-otp/', VerifyRecruiterOTPView.as_view(), name='verify-recruiter-otp'),

    # ✅ Dashboard - Recent Opportunities
    path('dashboard/opportunities/', RecruiterDashboardOpportunitiesView.as_view(), name='recruiter-dashboard-opportunities'),
    path('dashboard/', RecruiterDashboardStatsView.as_view(), name='recruiter-dashboard-stats'),

]
