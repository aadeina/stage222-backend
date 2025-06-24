import re
from rest_framework import serializers
from .models import RecruiterProfile

class RecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruiterProfile
        exclude = ['user']  # still excluded from POST/PATCH input
        read_only_fields = ['is_verified']  # only admin can toggle verification

    # def validate_phone(self, value):
    #     """
    #     Validate Mauritanian recruiter phone numbers starting with:
    #     +2222 (Chinguitel), +2223 (Mattel), +2224 (Mauritel)
    #     """
    #     pattern = r'^\+222(2|3|4)\d{7}$'
    #     if not re.match(pattern, value):
    #         raise serializers.ValidationError(
    #             "Phone must be a valid Mauritanian number starting with +2222, +2223, or +2224 and followed by 7 digits."
    #         )
    #     return value

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
