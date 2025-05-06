# candidates/urls.py
from django.urls import path
from .views import (
    CandidateMeView,
    CandidateDetailView,
    CandidateResumeUploadView
)

urlpatterns = [
    # Candidate's own profile (GET, PUT)
    path('me/', CandidateMeView.as_view(), name='candidate-me'),

    # Public profile view by ID
    path('<uuid:pk>/', CandidateDetailView.as_view(), name='candidate-detail'),

    # Resume upload endpoint
    path('me/resume/', CandidateResumeUploadView.as_view(), name='upload-resume'),
]
