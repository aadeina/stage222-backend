from django.urls import path
from .views import (
    CandidateMeView,
    CandidateDetailView,
    CandidateResumeUploadView,
    SkillListView,
    CandidateSkillUpdateView
)

urlpatterns = [
    # 🧑‍💻 Candidate's own profile (GET, PUT)
    path('me/', CandidateMeView.as_view(), name='candidate-me'),

    # 📄 Resume upload
    path('me/resume/', CandidateResumeUploadView.as_view(), name='upload-resume'),

    # 🧠 Skill management
    path('skills/', SkillListView.as_view(), name='skill-list'),
    path('me/skills/', CandidateSkillUpdateView.as_view(), name='candidate-skill-update'),

    # 🌐 Public profile view
    path('<uuid:pk>/', CandidateDetailView.as_view(), name='candidate-detail'),
]
