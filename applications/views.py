from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import Application
from .serializers import ApplicationSerializer, ApplicationUpdateSerializer
from accounts.permissions import IsCandidate, IsRecruiter
from internships.models import Internship


# 🎓 Candidate applies to an internship
class InternshipApplyView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsCandidate]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"id": self.kwargs.get("id")})
        return context


# 🧠 Recruiter lists applications for internships they posted (with optional filters)
class ApplicationListView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def get_queryset(self):
        recruiter = self.request.user.recruiter
        queryset = Application.objects.filter(internship__recruiter=recruiter)

        # ✅ Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter in ['pending', 'accepted', 'rejected']:
            queryset = queryset.filter(status=status_filter)

        # ✅ Filter by shortlisted
        shortlisted = self.request.query_params.get('shortlisted')
        if shortlisted == 'true':
            queryset = queryset.exclude(shortlisted_at__isnull=True)
        elif shortlisted == 'false':
            queryset = queryset.filter(shortlisted_at__isnull=True)

        return queryset



# ✏️ Recruiter updates application status
class ApplicationUpdateView(generics.UpdateAPIView):
    serializer_class = ApplicationUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]
    lookup_field = 'id'

    def get_queryset(self):
        return Application.objects.filter(internship__recruiter=self.request.user.recruiter)


# ✅ Recruiter shortlists a candidate manually
class ShortlistApplicationView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def post(self, request, id):
        application = get_object_or_404(Application, id=id)

        # 🔐 Check recruiter owns the internship
        if application.internship.recruiter.user != request.user:
            raise PermissionDenied("You're not authorized to modify this application.")

        if application.shortlisted_at:
            return Response({"message": "Candidate already shortlisted."}, status=200)

        application.mark_shortlisted()  # ✅ Uses model method
        serializer = ApplicationSerializer(application)
        return Response({
            "message": "Candidate successfully shortlisted.",
            "application": serializer.data
        }, status=status.HTTP_200_OK)


# 📌 View applicants for a specific internship (recruiter only)
class InternshipApplicantsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def get_queryset(self):
        internship_id = self.kwargs.get('internship_id')
        recruiter = self.request.user.recruiter

        # Validate ownership
        internship = get_object_or_404(
            Internship, id=internship_id, recruiter=recruiter
        )

        return Application.objects.filter(internship=internship)


# ==========================
# 🧑‍🎓 Candidate Views Below
# ==========================

# 📄 List all applications of the candidate
class ApplicationListForCandidateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCandidate]

    def get(self, request):
        apps = Application.objects.filter(candidate=request.user.candidate).select_related('internship').order_by('-created_at')
        serializer = ApplicationSerializer(apps, many=True)
        return Response(serializer.data)


# 🔢 Count of applications for the candidate
class ApplicationCountView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCandidate]

    def get(self, request):
        count = Application.objects.filter(candidate=request.user.candidate).count()
        return Response({"count": count})


# 🕒 Most recent 5 applications
class RecentApplicationsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCandidate]

    def get(self, request):
        apps = Application.objects.filter(candidate=request.user.candidate).select_related('internship').order_by('-created_at')[:5]
        serializer = ApplicationSerializer(apps, many=True)
        return Response(serializer.data)
