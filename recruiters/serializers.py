import re
from rest_framework import serializers
from .models import RecruiterProfile

class RecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruiterProfile
        exclude = ['user']  # we set this manually in views
        read_only_fields = ['is_verified', 'is_onboarded']  # onboarding flag controlled in backend

def validate_phone(self, value):
    """
    Validate Mauritanian recruiter phone numbers:
    - Must be exactly 8 digits
    - Must start with 2, 3, or 4
    """
    pattern = r'^[234]\d{7}$'
    if not re.match(pattern, value):
        raise serializers.ValidationError(
            "Phone number must be exactly 8 digits and start with 2, 3, or 4 (Mauritel, Mattel, or Chinguitel)."
        )
    return value
