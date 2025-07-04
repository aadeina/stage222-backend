from django.urls import path
from .views import (
    InternshipApplyView,
    ApplicationListView,
    ApplicationUpdateView,
    ShortlistApplicationView,
    InternshipApplicantsView,

    # ✅ Candidate views
    ApplicationListForCandidateView,
    ApplicationCountView,
    RecentApplicationsView,
)

urlpatterns = [
    # 🎓 Candidate applies to internship
    path('internships/<uuid:id>/apply/', InternshipApplyView.as_view(), name='internship-apply'),

    # 🧠 Recruiter views
    path('recruiter/', ApplicationListView.as_view(), name='application-list'),
    path('<uuid:id>/update/', ApplicationUpdateView.as_view(), name='application-update'),
    path('<uuid:id>/shortlist/', ShortlistApplicationView.as_view(), name='application-shortlist'),
    path('internships/<uuid:internship_id>/applicants/', InternshipApplicantsView.as_view(), name='internship-applicants'),

    # 🧑‍🎓 Candidate views
    path('candidate/', ApplicationListForCandidateView.as_view(), name='candidate-applications'),
    path('candidate/count/', ApplicationCountView.as_view(), name='candidate-applications-count'),
    path('candidate/recent/', RecentApplicationsView.as_view(), name='candidate-recent-applications'),
]
