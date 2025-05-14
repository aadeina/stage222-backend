from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from django.shortcuts import get_object_or_404

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
# ✅ Recruiter lists applications with filter support
class ApplicationListView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def get_queryset(self):
        recruiter = self.request.user.recruiter
        queryset = Application.objects.filter(internship__recruiter=recruiter)

        # 🔍 Filter by ?shortlisted=true/false
        shortlisted_param = self.request.query_params.get('shortlisted')
        if shortlisted_param is not None:
            if shortlisted_param.lower() == 'true':
                queryset = queryset.filter(shortlisted=True)
            elif shortlisted_param.lower() == 'false':
                queryset = queryset.filter(shortlisted=False)

        # 🔍 Filter by ?status=pending/accepted/rejected
        status_param = self.request.query_params.get('status')
        if status_param in ['pending', 'accepted', 'rejected']:
            queryset = queryset.filter(status=status_param)

        return queryset



# ✅ Recruiter updates application status or shortlist
class ApplicationUpdateView(generics.UpdateAPIView):
    serializer_class = ApplicationUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]
    lookup_field = 'id'

    def get_queryset(self):
        recruiter = self.request.user.recruiter
        return Application.objects.filter(internship__recruiter=recruiter)

class ShortlistApplicationView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def post(self, request, id):
        application = get_object_or_404(Application, id=id)

        # 🚫 Check recruiter owns the internship
        if application.internship.recruiter.user != request.user:
            raise PermissionDenied("You're not authorized to shortlist this application.")

        # ✅ Mark as shortlisted
        if application.shortlisted:
            return Response({"message": "Already shortlisted."}, status=200)

        application.shortlisted = True
        application.shortlisted_at = timezone.now()
        application.save()

        return Response({
            "message": "Candidate successfully shortlisted.",
            "application": ApplicationSerializer(application).data
        }, status=200)