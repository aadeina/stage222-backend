from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from candidates.models import CandidateProfile
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from decouple import config

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
from core.ratelimits import limit_login, limit_register, limit_change_password, limit_password_reset, limit_password_reset_request

token_generator = PasswordResetTokenGenerator()

# ✅ Register with email verification
@limit_register()
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        verify_url = f"{settings.FRONTEND_URL}/verify-email/?uid={uid}&token={token}"

        send_mail(
            subject="Verify your email for Stage222",
            message=f"Click the link to verify your email: {verify_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

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
                'role': user.role,
                'is_verified': user.is_verified
            }
        })

# 👤 User Profile
class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

# 🔐 Change Password
@limit_change_password()
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

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

class ResendEmailVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResendEmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
            if user.is_verified:
                return Response({'detail': 'Email is already verified.'}, status=status.HTTP_400_BAD_REQUEST)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            verify_url = f"{config('FRONTEND_URL')}/api/auth/verify-email/?uid={uid}&token={token}"
            send_mail(
                subject="Verify your email for Stage222",
                message=f"Click the link to verify your email: {verify_url}",
                from_email=config("EMAIL_HOST_USER"),
                recipient_list=[user.email],
                fail_silently=False,
            )

            return Response({'detail': 'Verification email resent.'}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'detail': 'No user found with this email.'}, status=status.HTTP_404_NOT_FOUND)

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
            token = default_token_generator.make_token(user)
            reset_url = f"{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}"

            send_mail(
                subject="Reset your password - Stage222",
                message=f"Click to reset your password: {reset_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except User.DoesNotExist:
            pass  # Don't reveal existence of email

        return Response({"detail": "If the email is valid, a reset link has been sent."})

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
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({"detail": "Password reset successful."})
            else:
                return Response({"detail": "Invalid or expired token."}, status=400)
        except User.DoesNotExist:
            return Response({"detail": "Invalid user."}, status=400)

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_framework.exceptions import PermissionDenied

class CandidateOnlySocialLoginView(SocialLoginView):
    def process_login(self):
        user = self.user
        if user.role != 'candidate':
            raise PermissionDenied("Only candidates can log in with Google/Facebook.")
        return super().process_login()

class GoogleCandidateLogin(CandidateOnlySocialLoginView):
    adapter_class = GoogleOAuth2Adapter

class FacebookCandidateLogin(CandidateOnlySocialLoginView):
    adapter_class = FacebookOAuth2Adapter



class GoogleLoginJWT(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def get_response(self):
        user = self.user

        # 🔐 Auto-create CandidateProfile if needed
        if user.role == 'candidate' and not hasattr(user, 'candidate'):
            CandidateProfile.objects.create(user=user)

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": str(user.id),
                "email": user.email,
                "role": user.role,
                "is_verified": user.is_verified
            }
        })
