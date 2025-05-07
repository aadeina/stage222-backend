from django.urls import path
from .views import InternshipApplyView

urlpatterns = [
    path('internships/<uuid:internship_id>/apply/', InternshipApplyView.as_view(), name='internship-apply'),
]
