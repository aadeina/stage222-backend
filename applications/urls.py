from django.urls import path
from .views import (
    InternshipApplyView,
    ApplicationListView,
    ApplicationUpdateView,
    ShortlistApplicationView,
    InternshipApplicantsView
)

urlpatterns = [
    # 🎓 Candidate applies to an internship
    path(
        'internships/<uuid:id>/apply/',
        InternshipApplyView.as_view(),
        name='application-apply'
    ),

    # 🧠 Recruiter lists all applications to their internships
    path(
        'recruiter/applications/',
        ApplicationListView.as_view(),
        name='application-list'
    ),

    # ✏️ Recruiter updates application status (accept/reject)
    path(
        'recruiter/applications/<uuid:id>/update/',
        ApplicationUpdateView.as_view(),
        name='application-update'
    ),

    # 🌟 Recruiter shortlists a candidate
    path(
        'recruiter/applications/<uuid:id>/shortlist/',
        ShortlistApplicationView.as_view(),
        name='application-shortlist'
    ),
        # 👁️‍🗨️ View all applicants for one internship (used for eye icon in UI)
    path(
        'recruiter/internships/<uuid:internship_id>/applicants/',
        InternshipApplicantsView.as_view(),
        name='internship-applicants'
    ),
]
