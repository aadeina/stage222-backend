from django.urls import path
from .views import InternshipApplyView, ApplicationListView, ApplicationUpdateView

urlpatterns = [
    path('<uuid:id>/apply/', InternshipApplyView.as_view(), name='internship-apply'),
    path('', ApplicationListView.as_view(), name='application-list'),
    path('<uuid:id>/', ApplicationUpdateView.as_view(), name='application-update'),
]
