from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from .models import User, Admin
from recruiters.models import RecruiterProfile

# ✅ User Registration (Candidate or Generic)
class RegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phone_number', 'role']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



# ✅ Recruiter Registration (Dedicated Flow)
class RecruiterRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, validators=[validate_password])
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(
        required=True,
        validators=[RegexValidator(regex=r'^[234]\d{7}$', message="Enter a valid 8-digit Mauritanian number.")]
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'phone_number', 'first_name', 'last_name']

    def create(self, validated_data):
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        phone_number = validated_data.pop('phone_number')

        user = User.objects.create_user(
            role='recruiter',
            phone_number=phone_number,
            **validated_data
        )
        RecruiterProfile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
        )
        return user


# 🔐 Login
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        if not user.is_active:
            raise serializers.ValidationError("Account disabled.")
        return {'user': user}


# 👤 User Profile
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'is_verified', 'created_at']
        read_only_fields = ['id', 'email', 'role', 'created_at']


# 🔐 Change Password
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


# 🔁 Email Verification & Password Reset
class ResendEmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)

def validate_phone_number(self, value):
    if RecruiterProfile.objects.filter(phone=value).exists():
        raise serializers.ValidationError("Recruiter with this phone number already exists.")
    return value


# 🛡️ Admin Control
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        exclude = ['user']
