from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Application
from .serializers import ApplicationSerializer, ApplicationUpdateSerializer
from accounts.permissions import IsCandidate, IsRecruiter

# ✅ Candidate applies to an internship
class InternshipApplyView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsCandidate]

    def perform_create(self, serializer):
        internship_id = self.kwargs.get("id")
        candidate = self.request.user.candidate
        serializer.save(candidate=candidate, internship_id=internship_id)


# ✅ Recruiter lists applications for internships they posted
class ApplicationListView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def get_queryset(self):
        recruiter = self.request.user.recruiter
        return Application.objects.filter(internship__recruiter=recruiter)


# ✅ Recruiter updates application status or shortlist
class ApplicationUpdateView(generics.UpdateAPIView):
    serializer_class = ApplicationUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]
    lookup_field = 'id'

    def get_queryset(self):
        recruiter = self.request.user.recruiter
        return Application.objects.filter(internship__recruiter=recruiter)
