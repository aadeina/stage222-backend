from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import RecruiterProfile
from .serializers import RecruiterSerializer
from accounts.permissions import IsRecruiter  # Must exist
from rest_framework.permissions import IsAuthenticated

class RecruiterMeView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiter]

    def get(self, request):
        try:
            recruiter = request.user.recruiter
            serializer = RecruiterSerializer(recruiter)
            return Response(serializer.data)
        except RecruiterProfile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        if hasattr(request.user, 'recruiter'):
            return Response({"detail": "Profile already exists."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = RecruiterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            recruiter = request.user.recruiter
        except RecruiterProfile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = RecruiterSerializer(recruiter, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecruiterDetailView(generics.RetrieveAPIView):
    queryset = RecruiterProfile.objects.all()
    serializer_class = RecruiterSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "user__id"
