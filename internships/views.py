from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import Internship
from .serializers import InternshipSerializer
from accounts.permissions import IsRecruiter, IsCandidate
from applications.models import Application
from applications.serializers import ApplicationSerializer

# 🎯 Recruiter-only: Post internship (approval defaults to pending)
class InternshipCreateView(generics.CreateAPIView):
    serializer_class = InternshipSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def perform_create(self, serializer):
        recruiter = self.request.user.recruiter
        serializer.save(
            recruiter=recruiter,
            organization=recruiter.organization
        )


# 🌍 Public: List only approved + open internships
class InternshipListView(generics.ListAPIView):
    serializer_class = InternshipSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'location', 'description']
    ordering_fields = ['start_date', 'stipend', 'deadline']

    def get_queryset(self):
        return Internship.objects.filter(
            approval_status='approved',
            status='open'
        ).order_by('-created_at')


# 🛠️ Detail view: Recruiters can update/delete, public can view
class InternshipDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsRecruiter()]
        return [permissions.AllowAny()]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "✅ Internship deleted successfully."},
            status=status.HTTP_200_OK
        )


# 📨 Candidate-only: Apply to internship
class ApplyToInternshipView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsCandidate]

    def perform_create(self, serializer):
        internship = get_object_or_404(Internship, id=self.kwargs["id"])

        if internship.approval_status != 'approved':
            raise ValidationError({"detail": "❌ This internship is not approved."})

        if internship.status != 'open':
            raise ValidationError({"detail": "❌ This internship is currently closed."})

        candidate = self.request.user.candidate
        serializer.save(candidate=candidate, internship=internship)
