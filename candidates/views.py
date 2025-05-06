from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CandidateProfile
from .serializers import CandidateSerializer
from accounts.permissions import IsCandidate

# 🔒 Permission: Candidate Only
class IsCandidate(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'candidate'

# 👤 /api/candidates/me/ → GET, POST (create), PUT (update)
class CandidateMeView(APIView):
    permission_classes = [IsAuthenticated, IsCandidate]

    def get(self, request):
        try:
            candidate = request.user.candidate
            serializer = CandidateSerializer(candidate)
            return Response(serializer.data)
        except CandidateProfile.DoesNotExist:
            return Response({"detail": "No profile found. Please create one."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        if hasattr(request.user, 'candidate'):
            return Response({"detail": "Profile already exists."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            candidate = request.user.candidate
        except CandidateProfile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CandidateSerializer(candidate, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 👤 /api/candidates/<uuid:pk>/ → GET Public Profile by ID
class CandidateDetailView(generics.RetrieveAPIView):
    queryset = CandidateProfile.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [permissions.AllowAny]

# 📄 /api/candidates/me/resume/ → POST Upload PDF Resume
MAX_RESUME_SIZE_MB = 2  # you can put this in settings.py later

class CandidateResumeUploadView(APIView):
    permission_classes = [IsAuthenticated, IsCandidate]

    def post(self, request):
        try:
            candidate = request.user.candidate
        except CandidateProfile.DoesNotExist:
            return Response({"detail": "Candidate profile not found."}, status=status.HTTP_404_NOT_FOUND)

        resume = request.FILES.get('resume')
        if not resume:
            return Response({"detail": "No resume file provided."}, status=status.HTTP_400_BAD_REQUEST)

        if resume.content_type != 'application/pdf':
            return Response({"detail": "Resume must be a PDF file."}, status=status.HTTP_400_BAD_REQUEST)

        if resume.size > MAX_RESUME_SIZE_MB * 1024 * 1024:
            return Response(
                {"detail": f"Resume file is too large. Max size is {MAX_RESUME_SIZE_MB}MB."},
                status=status.HTTP_400_BAD_REQUEST
            )

        candidate.resume = resume
        candidate.save()
        return Response({"detail": "Resume uploaded successfully."}, status=status.HTTP_200_OK)

