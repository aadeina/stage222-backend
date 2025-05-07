from rest_framework import generics, permissions
from .models import Application
from .serializers import ApplicationSerializer
from accounts.permissions import IsCandidate

class InternshipApplyView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsCandidate]
