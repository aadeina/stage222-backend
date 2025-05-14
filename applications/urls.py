from django.urls import path
from .views import (
    InternshipApplyView,
    ApplicationListView,
    ApplicationUpdateView,
    ShortlistApplicationView,  # ✅ Import new view
)

urlpatterns = [
    path('<uuid:id>/apply/', InternshipApplyView.as_view(), name='internship-apply'),
    path('', ApplicationListView.as_view(), name='application-list'),
    path('<uuid:id>/', ApplicationUpdateView.as_view(), name='application-update'),
    path('<uuid:id>/shortlist/', ShortlistApplicationView.as_view(), name='application-shortlist'),
]
