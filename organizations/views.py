from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Organization
from .serializers import OrganizationSerializer
from accounts.permissions import IsRecruiter

# 🔍 Public list of all organizations
class OrganizationListView(generics.ListAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.AllowAny]


# 🌐 Public detail view of an organization by UUID
class OrganizationDetailView(generics.RetrieveAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'


# 🏢 Create a new organization (only one per recruiter)
class OrganizationCreateView(generics.CreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def create(self, request, *args, **kwargs):
        recruiter = request.user.recruiter

        if recruiter.organization:
            raise ValidationError("❌ You already have an organization linked to your profile.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organization = serializer.save()

        # Link to recruiter
        recruiter.organization = organization

        # Auto-verify if all methods provided
        if (
            organization.license_document and
            organization.website and
            organization.social_links
        ):
            recruiter.is_verified = True

        recruiter.save()

        return Response({
            "status": "success",
            "message": "🎉 Organization created successfully. Redirecting to post opportunity...",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


# ✏️ Update organization (only by owning recruiter)
class OrganizationUpdateView(generics.UpdateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        org = self.get_object()
        recruiter = request.user.recruiter

        if recruiter.organization != org:
            raise ValidationError("❌ You are not allowed to update this organization.")

        serializer = self.get_serializer(org, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_org = serializer.save()

        # Re-check verification if fields changed
        if (
            updated_org.license_document and
            updated_org.website and
            updated_org.social_links
        ):
            recruiter.is_verified = True
            recruiter.save()

        return Response({
            "status": "success",
            "message": "✅ Organization updated successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
