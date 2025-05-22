# views.py (to be placed in your recruiters/views.py)

import random
import requests
from django.conf import settings
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from .models import RecruiterProfile
from .serializers import RecruiterSerializer
from accounts.models import User
from accounts.permissions import IsRecruiter
from rest_framework.permissions import IsAuthenticated
from core.ratelimits import limit_recruiter_send_otp, limit_recruiter_verify_otp

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


@method_decorator(limit_recruiter_send_otp(), name='dispatch')
class SendRecruiterOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        phone = request.data.get("phone")
        lang = request.data.get("lang", "fr")

        if not phone:
            return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

        code = str(random.randint(100000, 999999))

        try:
            recruiter = RecruiterProfile.objects.get(phone=phone)
            recruiter.verification_code = code
            recruiter.save()
        except RecruiterProfile.DoesNotExist:
            return Response({"error": "Recruiter not found for this phone number."}, status=status.HTTP_404_NOT_FOUND)

        response = requests.post(
            f"https://chinguisoft.com/api/sms/validation/{settings.CHINGUISOFT_VALIDATION_KEY}",
            headers={
                "Validation-token": settings.CHINGUISOFT_VALIDATION_TOKEN,
                "Content-Type": "application/json"
            },
            json={"phone": phone, "lang": lang, "code": code}
        )

        if response.status_code == 200:
            return Response({"message": "OTP sent successfully."})
        else:
            return Response(response.json(), status=response.status_code)


@method_decorator(limit_recruiter_verify_otp(), name='dispatch')
class VerifyRecruiterOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        phone = request.data.get("phone")
        otp = request.data.get("otp")

        if not all([phone, otp]):
            return Response({"error": "Phone and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            recruiter = RecruiterProfile.objects.get(phone=phone)
        except RecruiterProfile.DoesNotExist:
            return Response({"error": "Recruiter not found."}, status=status.HTTP_404_NOT_FOUND)

        if recruiter.verification_code == otp:
            recruiter.is_verified = True
            recruiter.verification_code = None
            recruiter.save()
            return Response({"message": "Phone number verified successfully."})
        else:
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
