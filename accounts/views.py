import uuid
from datetime import timedelta
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.mail import send_mail
from core.email_utils import send_otp_email
from django.utils.timezone import now
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework import status, generics, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from decouple import config

from accounts.models import User, EmailOTP, OTPAttempt
from candidates.models import CandidateProfile

from accounts.models import User
from accounts.serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    ChangePasswordSerializer,
    ResendEmailVerificationSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer
)

from core.ratelimits import (
    limit_login,
    limit_register,
    limit_change_password,
    limit_password_reset,
    limit_password_reset_request
)


# ✅ Register with email verification + auto candidate profile

import random
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from candidates.models import CandidateProfile

from core.email_utils import send_otp_email
from accounts.models import EmailOTP
from accounts.serializers import RegisterSerializer

User = get_user_model()

def generate_otp():
    return str(random.randint(100000, 999999))

@limit_register()
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if user.role == 'candidate' and not hasattr(user, 'candidate'):
            CandidateProfile.objects.create(user=user)

        # OTP & token setup
        otp = generate_otp()
        EmailOTP.objects.create(user=user, otp_code=otp)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        verify_url = f"https://stage222.com/verify-email/?uid={uid}&token={token}"

        # Send SendGrid HTML email
        send_otp_email(
            to_email=user.email,
            user_name=user.first_name,
            otp_code=otp,
            verify_url=verify_url
        )

        return Response({"message": "OTP verification email sent!"}, status=status.HTTP_201_CREATED)



# 🔐 Login
@limit_login()
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': str(user.id),
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'is_verified': user.is_verified
            }
        })


# 👤 User Profile
class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# 🔐 Change Password
@limit_change_password()
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)


# 🚪 Logout
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ✅ Email Verification
class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        uid = request.GET.get('uid')
        token = request.GET.get('token')

        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)

            if token_generator.check_token(user, token):
                user.is_verified = True
                user.save()
                return Response({"detail": "Email verified successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"detail": "Invalid verification link."}, status=status.HTTP_400_BAD_REQUEST)


# 🔁 Resend Email Verification

class ResendEmailVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResendEmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
            if user.is_verified:
                return Response({'detail': 'Email is already verified.'}, status=400)

            otp = generate_otp()
            EmailOTP.objects.create(user=user, otp_code=otp)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            verify_url = f"{settings.FRONTEND_URL}/verify-email/?uid={uid}&token={token}"

            send_otp_email(user.email, user.first_name, otp, verify_url)

            return Response({'detail': 'Verification email resent.'}, status=200)

        except User.DoesNotExist:
            return Response({'detail': 'No user found with this email.'}, status=404)



# 🔁 Request Password Reset
@limit_password_reset_request()
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            reset_url = f"{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}"

            send_mail(
                subject="Reset your password - Stage222",
                message=f"Click to reset your password: {reset_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except User.DoesNotExist:
            pass  # Do not leak user existence

        return Response({"detail": "If the email is valid, a reset link has been sent."})


# 🔁 Reset Password via Token
@limit_password_reset()
class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = force_str(urlsafe_base64_decode(serializer.validated_data['uid']))
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        try:
            user = User.objects.get(pk=uid)
            if token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({"detail": "Password reset successful."})
            else:
                return Response({"detail": "Invalid or expired token."}, status=400)
        except User.DoesNotExist:
            return Response({"detail": "Invalid user."}, status=400)

# 🌐 Social Login (Candidates Only)
class CandidateOnlySocialLoginView(SocialLoginView):
    def process_login(self):
        user = self.user

        # Set default role if not yet assigned
        if not user.role:
            user.role = 'candidate'
            user.save()

        # Prevent access only if role is set and not candidate
        if user.role != 'candidate':
            raise PermissionDenied("Only candidates can log in with Google/Facebook.")

        return super().process_login()


class GoogleCandidateLogin(CandidateOnlySocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class FacebookCandidateLogin(CandidateOnlySocialLoginView):
    adapter_class = FacebookOAuth2Adapter


# 🌐 Google Login With JWT Response
class GoogleLoginJWT(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def get_response(self):
        user = self.user

        # Set default role if missing
        if not user.role:
            user.role = 'candidate'
            user.save()

        # Auto-create CandidateProfile if needed
        if user.role == 'candidate' and not hasattr(user, 'candidate'):
            CandidateProfile.objects.create(user=user)

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": str(user.id),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "is_verified": user.is_verified
            }
        })

MAX_OTP_ATTEMPTS = 3  # ✅ Limit to 3
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        ip = request.META.get('REMOTE_ADDR') or 'unknown'

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Invalid email address."}, status=400)

        recent_attempts = OTPAttempt.objects.filter(
            user=user,
            timestamp__gte=timezone.now() - timedelta(minutes=10)
        )

        if recent_attempts.count() >= MAX_OTP_ATTEMPTS:
            OTPAttempt.objects.create(user=user, otp_code=otp, is_successful=False, ip_address=ip, email=email)
            return Response({"detail": "Too many attempts. Try again later."}, status=429)

        otp_entry = EmailOTP.objects.filter(user=user, otp_code=otp, is_used=False).order_by('-created_at').first()

        if not otp_entry:
            OTPAttempt.objects.create(user=user, otp_code=otp, is_successful=False, ip_address=ip, email=email)
            return Response({"detail": "Invalid OTP."}, status=400)

        if otp_entry.is_expired():
            OTPAttempt.objects.create(user=user, otp_code=otp, is_successful=False, ip_address=ip, email=email)
            return Response({"detail": "OTP expired."}, status=400)

        # Mark OTP used
        otp_entry.is_used = True
        otp_entry.save()

        # Mark verified
        user.is_verified = True
        user.save()

        # Log success
        OTPAttempt.objects.create(user=user, otp_code=otp, is_successful=True, ip_address=ip, email=email)

        # ✅ Auto-login
        refresh = RefreshToken.for_user(user)

        return Response({
            "detail": "Email verified successfully.",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": str(user.id),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "is_verified": user.is_verified
            }
        }, status=200)

RESEND_OTP_COOLDOWN_SECONDS = 60  # ⏱️ Limit resending to once per 60 seconds

from accounts.views import generate_otp  # reuse from your register logic

RESEND_COOLDOWN_SECONDS = 60  # ⏱️ Cooldown limit

class ResendOTPVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"detail": "Email is required."}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "No user found with this email."}, status=404)

        if user.is_verified:
            return Response({"detail": "✅ Email already verified."}, status=400)

        latest_otp = EmailOTP.objects.filter(user=user).order_by('-created_at').first()
        if latest_otp and (timezone.now() - latest_otp.created_at) < timedelta(seconds=RESEND_COOLDOWN_SECONDS):
            seconds_left = RESEND_COOLDOWN_SECONDS - int((timezone.now() - latest_otp.created_at).total_seconds())
            return Response(
                {"detail": f"⏳ Please wait {seconds_left} seconds before requesting another OTP."},
                status=429
            )

        # generate + send new OTP
        otp = generate_otp()
        EmailOTP.objects.create(user=user, otp_code=otp)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        verify_url = f"https://stage222.com/verify-email/?uid={uid}&token={token}"

        send_otp_email(
            to_email=user.email,
            user_name=user.first_name,
            otp_code=otp,
            verify_url=verify_url
        )

        return Response({"detail": "📩 Verification OTP resent."}, status=200)
