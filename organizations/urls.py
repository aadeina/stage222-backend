from django.urls import path
from .views import (
    OrganizationListView,
    OrganizationDetailView,
    OrganizationCreateView,
    OrganizationUpdateView,
)

urlpatterns = [
    # 🔍 Public: List all organizations
    path('', OrganizationListView.as_view(), name='organization-list'),

    # 🌐 Public: Get one organization by UUID
    path('<uuid:id>/', OrganizationDetailView.as_view(), name='organization-detail'),

    # 🏢 Recruiter/Admin: Create a new organization
    path('create/', OrganizationCreateView.as_view(), name='organization-create'),

    # ✏️ Recruiter-only: Update an organization (must be owner)
    path('<uuid:id>/update/', OrganizationUpdateView.as_view(), name='organization-update'),
]
