from django.urls import path
from .views import (
    InternshipCreateView,
    InternshipListView,
    MyInternshipsView,
    InternshipApprovalView,
    InternshipDetailView,
    ApplyToInternshipView,
)

urlpatterns = [
    # 🌍 Public: View all approved + open internships
    path('', InternshipListView.as_view(), name='internship-list'),

    # 🧑‍💼 Recruiter: Post a new internship (auto status = pending)
    path('create/', InternshipCreateView.as_view(), name='internship-create'),

    # 🧑‍💼 Recruiter: View all internships they created
    path('me/', MyInternshipsView.as_view(), name='my-internships'),

    # 📄 Public: View internship details
    # ✏️ Recruiter: Update/delete if owner
    path('<uuid:id>/', InternshipDetailView.as_view(), name='internship-detail'),

    # 📩 Candidate: Apply to an internship
    path('<uuid:id>/apply/', ApplyToInternshipView.as_view(), name='internship-apply'),

    # ✅ Admin: Approve or reject internship (with reason)
    path('<uuid:id>/approve/', InternshipApprovalView.as_view(), name='internship-approve'),
]
