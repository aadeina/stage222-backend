from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Organization
from .serializers import OrganizationSerializer
from accounts.permissions import IsRecruiter


# 🔍 List all organizations (public)
class OrganizationListView(generics.ListAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.AllowAny]


# 🌐 Retrieve a single organization by UUID (public)
class OrganizationDetailView(generics.RetrieveAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'


# 🏢 Create a new organization (one per recruiter)
class OrganizationCreateView(generics.CreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def perform_create(self, serializer):
        recruiter = self.request.user.recruiter

        if recruiter.organization:
            raise ValidationError("❌ You already have an organization linked to your profile.")

        organization = serializer.save()
        recruiter.organization = organization
        recruiter.save()


# ✏️ Update organization info (owner-only)
class OrganizationUpdateView(generics.UpdateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]
    lookup_field = 'id'

    def perform_update(self, serializer):
        org = self.get_object()
        recruiter = self.request.user.recruiter

        if recruiter.organization != org:
            raise ValidationError("❌ You are not allowed to update this organization.")

        serializer.save()
