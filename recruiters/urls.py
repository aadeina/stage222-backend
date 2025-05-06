from django.urls import path
from .views import RecruiterMeView, RecruiterDetailView

urlpatterns = [
    path('me/', RecruiterMeView.as_view(), name='recruiter-me'),
    path('<uuid:user__id>/', RecruiterDetailView.as_view(), name='recruiter-detail'),
]
