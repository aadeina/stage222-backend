from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from .models import Internship
from .serializers import InternshipSerializer
from accounts.permissions import IsRecruiter, IsCandidate
from applications.models import Application
from applications.serializers import ApplicationSerializer
from django.shortcuts import get_object_or_404

# ✅ Create Internship (Recruiter only)
class InternshipCreateView(generics.CreateAPIView):
    serializer_class = InternshipSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def perform_create(self, serializer):
        recruiter = self.request.user.recruiter
        serializer.save(recruiter=recruiter, organization=recruiter.organization)


# ✅ List Internships (Open Only)
class InternshipListView(generics.ListAPIView):
    queryset = Internship.objects.filter(status='open')
    serializer_class = InternshipSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'location', 'description']
    ordering_fields = ['start_date', 'stipend', 'deadline']


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
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

class ApplyToInternshipView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsCandidate]

    def perform_create(self, serializer):
        try:
            internship = get_object_or_404(Internship, id=self.kwargs["id"])
            candidate = self.request.user.candidate
            serializer.save(candidate=candidate, internship=internship)
        except Exception as e:
            raise ValidationError({"detail": f"❌ Application failed: {str(e)}"})
