from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Internship
from .serializers import InternshipSerializer
from accounts.permissions import IsRecruiter, IsCandidate, IsAdmin
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


# 🔒 Recruiter-only: List their posted internships
class MyInternshipsView(generics.ListAPIView):
    serializer_class = InternshipSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def get_queryset(self):
        return Internship.objects.filter(recruiter=self.request.user.recruiter)


# 🔐 Admin-only: Approve or reject internships
class InternshipApprovalView(generics.UpdateAPIView):
    serializer_class = InternshipSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    queryset = Internship.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        internship = self.get_object()
        status_choice = request.data.get("approval_status")
        rejection_reason = request.data.get("rejection_reason", None)

        if status_choice not in ['approved', 'rejected']:
            return Response({"error": "Invalid approval status."}, status=400)

        internship.approval_status = status_choice
        if status_choice == 'rejected':
            internship.rejection_reason = rejection_reason
        internship.save()

        return Response({"message": f"Internship has been {status_choice}."}, status=200)


# 📄 Public & Recruiter: View, update, or delete internship
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
