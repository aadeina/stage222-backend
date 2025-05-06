import re
from rest_framework import serializers
from .models import RecruiterProfile

class RecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruiterProfile
        exclude = ['user']
        read_only_fields = ['is_verified']

    def validate_phone(self, value):
        pattern = r'^\+222(2|3|4)\d{7}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Phone must be a valid Mauritanian number starting with +2222, +2223, or +2224.")
        return value
