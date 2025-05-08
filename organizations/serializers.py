from rest_framework import serializers
from .models import Organization
from PIL import Image

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

    def validate_logo(self, value):
        if value:
            # ✅ Check size (max 1MB)
            if value.size > 1024 * 1024:
                raise serializers.ValidationError("Logo must be under 1MB.")

            # ✅ Check file type
            valid_types = ['image/jpeg', 'image/png']
            if value.content_type not in valid_types:
                raise serializers.ValidationError("Only PNG or JPEG logos are allowed.")

            # ✅ Check dimensions
            image = Image.open(value)
            max_width, max_height = 300, 300

            if image.width > max_width or image.height > max_height:
                raise serializers.ValidationError(
                    f"Logo must be max {max_width}px by {max_height}px. "
                    f"Your image is {image.width}px × {image.height}px."
                )

        return value
