from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import Internship
from .serializers import InternshipSerializer
from accounts.permissions import IsRecruiter, IsCandidate
from applications.models import Application
from applications.serializers import ApplicationSerializer

# ✅ Create Internship (Recruiter only — defaults to pending approval)
class InternshipCreateView(generics.CreateAPIView):
    serializer_class = InternshipSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def perform_create(self, serializer):
        recruiter = self.request.user.recruiter
        serializer.save(recruiter=recruiter, organization=recruiter.organization)
        # approval_status will default to 'pending'


# ✅ List Internships (Only Approved + Open for public)
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


# ✅ Retrieve, Update, Delete Internship (Recruiter only for update/delete)
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


# ✅ Apply to Internship (Candidate only)
class ApplyToInternshipView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsCandidate]

    def perform_create(self, serializer):
        try:
            internship = get_object_or_404(Internship, id=self.kwargs["id"])

            if internship.approval_status != 'approved':
                raise ValidationError({"detail": "❌ This internship is not approved."})

            candidate = self.request.user.candidate
            serializer.save(candidate=candidate, internship=internship)

        except Exception as e:
            raise ValidationError({"detail": f"❌ Application failed: {str(e)}"})
