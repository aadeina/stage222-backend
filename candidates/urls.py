from django.urls import path
from .views import (
    CandidateMeView,
    CandidateDetailView,
    CandidateResumeUploadView,
    SkillListView,
    CandidateSkillUpdateView,
    SkillCreateView,
    CandidateSkillRemoveView,
    CandidateListView,
)

urlpatterns = [
    # 🧑‍💻 Candidate's own profile (GET, PUT)
    path('me/', CandidateMeView.as_view(), name='candidate-me'),

    # 📄 Resume upload
    path('me/resume/', CandidateResumeUploadView.as_view(), name='upload-resume'),

    # 🧠 Skill management
    path('skills/add/', SkillCreateView.as_view(), name='skill-add'),                     # 🔐 Admin only
    path('skills/', SkillListView.as_view(), name='skill-list'),                          # 🔍 Autocomplete via ?q=
    path('me/skills/', CandidateSkillUpdateView.as_view(), name='candidate-skill-update'),  # ✏️ Add/remove all
    path('me/skills/<str:skill_name>/', CandidateSkillRemoveView.as_view(), name='candidate-skill-remove'),  # ❌ Remove one

    # 🌐 Public endpoints
    path('', CandidateListView.as_view(), name='candidate-list'),                         # 🌐 Filter candidates by skill
    path('<uuid:pk>/', CandidateDetailView.as_view(), name='candidate-detail'),           # 🌐 Public profile
]
