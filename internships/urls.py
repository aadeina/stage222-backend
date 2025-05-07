from django.urls import path
from .views import (
    InternshipCreateView,
    InternshipListView,
    InternshipDetailView,
    ApplyToInternshipView  # 👈 Add this import
)

urlpatterns = [
    path('create/', InternshipCreateView.as_view(), name='internship-create'),
    path('', InternshipListView.as_view(), name='internship-list'),
    path('<uuid:id>/', InternshipDetailView.as_view(), name='internship-detail'),
    path('<uuid:id>/apply/', ApplyToInternshipView.as_view(), name='internship-apply'),  # 👈 New
]
