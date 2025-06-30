# organizations/serializers.py

from rest_framework import serializers
from .models import Organization
from PIL import Image
from urllib.parse import urlparse
import json
from io import BytesIO # <-- NEW: Import BytesIO

class OrganizationSerializer(serializers.ModelSerializer):
    social_links = serializers.JSONField(required=False, allow_null=True)

    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'is_independent', 'about', 'city', 'industry',
            'employee_range', 'website', 'logo', 'license_document', 'social_links',
            "founded_year",         # ✅ newly added
            "phone_number",         # ✅ newly added
            "email",                # ✅ newly added
            "address",              # ✅ newly added
            "is_verified"
        ]

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)

        if 'social_links' in data:
            social_links_value = data['social_links']
            if isinstance(social_links_value, str):
                try:
                    ret['social_links'] = json.loads(social_links_value)
                except json.JSONDecodeError:
                    ret['social_links'] = [
                        url.strip() for url in social_links_value.split(',') if url.strip()
                    ]
            elif not isinstance(social_links_value, list):
                raise serializers.ValidationError(
                    {"social_links": "Social links must be a valid JSON array string or a comma-separated string."}
                )
        else:
            ret['social_links'] = []

        return ret


    def validate_logo(self, value):
        if value:
            # 1. Check size (max 10MB)
            if value.size > 10 * 1024 * 1024: # 10MB
                raise serializers.ValidationError("Logo must be under 10MB.")

            # 2. Check file type
            valid_types = ['image/jpeg', 'image/png', 'image/gif']
            if hasattr(value, 'content_type') and value.content_type not in valid_types:
                raise serializers.ValidationError("Only PNG, JPG, or GIF logos are allowed.")

            # 3. Validate image integrity using Pillow (Pro Method)
            # Read the content into an in-memory BytesIO object to allow Pillow to work
            # without issues related to Django's file handling or file pointer state.
            try:
                # IMPORTANT: Read the content of the uploaded file
                # The file might have been read once by DRF, so rewind before reading.
                value.seek(0)
                file_content = value.read()
                
                # Create an in-memory file-like object for Pillow
                img = Image.open(BytesIO(file_content))
                img.verify()  # Verify that it is an image
                # No need to img.close() for BytesIO, it will be garbage collected.

                # If you had dimension validation (currently commented out):
                # max_width, max_height = 300, 300
                # if img.width > max_width or img.height > max_height:
                #     raise serializers.ValidationError(
                #         f"Logo must be at most {max_width}x{max_height}px. "
                #         f"Your image is {img.width}x{img.height}px."
                #     )

            except (IOError, SyntaxError) as e:
                raise serializers.ValidationError(f"Invalid or corrupted image file: {e}")
            
            # After validation, ensure the file pointer is at the beginning for storage to read it correctly
            value.seek(0)

        return value

    def validate_license_document(self, value):
        if value:
            # 1. Check file size (max 10MB)
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError("License document must be under 10MB.")

            # 2. Check file type
            valid_types = ['application/pdf', 'image/jpeg', 'image/png', 'image/gif']
            if hasattr(value, 'content_type') and value.content_type not in valid_types:
                raise serializers.ValidationError("Only PDF, PNG, JPG, or GIF license documents allowed.")

            # 3. Optional: Basic image integrity for image types in license document
            if value.content_type in ['image/jpeg', 'image/png', 'image/gif']:
                try:
                    value.seek(0)
                    file_content = value.read() # Read content
                    img = Image.open(BytesIO(file_content)) # Use BytesIO
                    img.verify()
                    # No img.close() needed for BytesIO
                    value.seek(0) # Rewind for storage
                except (IOError, SyntaxError) as e:
                    raise serializers.ValidationError(f"Invalid or corrupted image file for license: {e}")
        return value

    def validate_social_links(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Social links must be a JSON list of URLs.")

        if len(value) > 3:
            raise serializers.ValidationError("Maximum 3 social media links are allowed.")

        for url in value:
            if not isinstance(url, str):
                raise serializers.ValidationError(f"Each social link must be a string: {url}")
            try:
                serializers.URLField().run_validation(url)
            except serializers.ValidationError:
                raise serializers.ValidationError(f"Invalid URL format for social link: {url}")
        return value

    def validate(self, data):
        has_license = data.get('license_document') is not None
        has_website = bool(data.get('website'))
        has_social_links = isinstance(data.get('social_links'), list) and len(data['social_links']) > 0

        if not (has_license or has_website or has_social_links):
            raise serializers.ValidationError(
                "Please complete at least one verification method (license, website, or social media)."
            )
        return data
    
def update(self, instance, validated_data):
    request = self.context.get('request')

    # ✅ Handle logo replacement
    if request and request.FILES.get('logo') and instance.logo:
        instance.logo.delete(save=False)

    # ✅ Handle license document replacement
    if request and request.FILES.get('license_document') and instance.license_document:
        instance.license_document.delete(save=False)

    return super().update(instance, validated_data)


