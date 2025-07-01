import re
from rest_framework import serializers
from .models import RecruiterProfile

class RecruiterSerializer(serializers.ModelSerializer):
    # 🔁 Add first_name and last_name as writable fields
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone = serializers.CharField(read_only=True)

    class Meta:
        model = RecruiterProfile
        exclude = ['user']
        read_only_fields = ['is_verified', 'is_onboarded']

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

    def update(self, instance, validated_data):
        # Handle nested user update
        user_data = validated_data.pop('user', {})
        instance = super().update(instance, validated_data)

        if user_data:
            user = instance.user
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.save()

        return instance
