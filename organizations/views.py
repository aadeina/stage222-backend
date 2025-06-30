from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Organization
from .serializers import OrganizationSerializer
from accounts.permissions import IsRecruiter

# 🔍 Public: List all organizations
class OrganizationListView(generics.ListAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.AllowAny]


# 🌐 Public: Get one organization by UUID
class OrganizationDetailView(generics.RetrieveAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'


# 🏢 Recruiter-only: Create a new organization
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

        recruiter.organization = organization

        if (
            organization.license_document and
            organization.website and
            organization.social_links
        ):
            recruiter.is_verified = True

        recruiter.save()

        return Response({
            "status": "success",
            "message": "🎉 Organization created successfully.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


# ✏️ Recruiter-only: Update an organization
from rest_framework.parsers import MultiPartParser, FormParser

class OrganizationUpdateView(generics.UpdateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]
    lookup_field = 'id'
    parser_classes = [MultiPartParser, FormParser]  # ✅ Required for file uploads

    def update(self, request, *args, **kwargs):
        org = self.get_object()
        recruiter = request.user.recruiter

        if recruiter.organization != org:
            raise ValidationError("❌ You are not allowed to update this organization.")

        serializer = self.get_serializer(org, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_org = serializer.save()

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



# 🙋‍♂️ Recruiter-only: Get current user's organization
class MyOrganizationView(generics.RetrieveAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def get_object(self):
        recruiter = self.request.user.recruiter
        return recruiter.organization
