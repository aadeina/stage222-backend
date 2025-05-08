from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser

from .models import CandidateProfile, Skill
from .serializers import (
    CandidateSerializer,
    SkillSerializer,
    CandidateSkillUpdateSerializer
)
from accounts.permissions import IsCandidate

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


# 🌐 /api/candidates/<uuid:pk>/ → GET Public Profile by ID
class CandidateDetailView(generics.RetrieveAPIView):
    queryset = CandidateProfile.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [permissions.AllowAny]


# 📄 /api/candidates/me/resume/ → POST Upload PDF Resume
MAX_RESUME_SIZE_MB = 2  # Consider moving to settings.py

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


# 🧠 /api/candidates/skills/ → List all available skills
class SkillListView(generics.ListAPIView):
    serializer_class = SkillSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Skill.objects.all()
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(name__icontains=q)
        return queryset



# 🧠 /api/candidates/me/skills/ → Add or update skills for candidate
class CandidateSkillUpdateView(generics.UpdateAPIView):
    serializer_class = CandidateSkillUpdateSerializer
    permission_classes = [IsAuthenticated, IsCandidate]

    def get_object(self):
        return self.request.user.candidate


# 🛠️ /api/candidates/skills/add/ → Admin creates a skill
class SkillCreateView(generics.CreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAdminUser]

    def get_serializer(self, *args, **kwargs):
        # Allow bulk creation
        if isinstance(kwargs.get('data'), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

class CandidateSkillRemoveView(APIView):
    permission_classes = [IsAuthenticated, IsCandidate]

    def delete(self, request, skill_name):
        try:
            candidate = request.user.candidate
            skill = Skill.objects.get(name=skill_name)
            candidate.skills.remove(skill)
            return Response({"detail": f"Skill '{skill_name}' removed."}, status=status.HTTP_200_OK)
        except Skill.DoesNotExist:
            return Response({"detail": "Skill not found."}, status=status.HTTP_404_NOT_FOUND)

class CandidateListView(generics.ListAPIView):
    serializer_class = CandidateSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = CandidateProfile.objects.all()
        skill_name = self.request.query_params.get('skills')
        if skill_name:
            qs = qs.filter(skills__name__iexact=skill_name)
        return qs
