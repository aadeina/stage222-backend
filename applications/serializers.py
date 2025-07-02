from rest_framework import serializers
from .models import Application
from internships.models import Internship


class ApplicationSerializer(serializers.ModelSerializer):
    screening_answers = serializers.JSONField(required=False)

    # 🧑‍💼 Recruiter-facing candidate details
    candidate_name = serializers.SerializerMethodField()
    candidate_email = serializers.SerializerMethodField()
    candidate_resume = serializers.SerializerMethodField()
    candidate_photo = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = [
            'id',
            'cover_letter',
            'screening_answers',
            'status',
            'shortlisted_at',
            'created_at',
            'candidate_name',
            'candidate_email',
            'candidate_resume',
            'candidate_photo',
        ]
        read_only_fields = fields

    def get_candidate_name(self, obj):
        return obj.candidate.user.get_full_name()

    def get_candidate_email(self, obj):
        return obj.candidate.user.email

    def get_candidate_resume(self, obj):
        resume = obj.candidate.resume
        request = self.context.get('request')
        if resume and hasattr(resume, 'url'):
            return request.build_absolute_uri(resume.url) if request else resume.url
        return None

    def get_candidate_photo(self, obj):
        # If you have profile_picture on candidate model
        photo = getattr(obj.candidate, 'profile_picture', None)
        request = self.context.get('request')
        if photo and hasattr(photo, 'url'):
            return request.build_absolute_uri(photo.url) if request else photo.url
        return None

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        internship_id = self.context['view'].kwargs.get("id")

        try:
            internship = Internship.objects.get(id=internship_id)
        except Internship.DoesNotExist:
            raise serializers.ValidationError("This internship does not exist.")

        if internship.status != "open":
            raise serializers.ValidationError("This internship is not open for applications.")

        if Application.objects.filter(candidate=user.candidate, internship=internship).exists():
            raise serializers.ValidationError("You have already applied to this internship.")

        self.internship = internship
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        internship = self.internship

        return Application.objects.create(
            candidate=user.candidate,
            internship=internship,
            cover_letter=validated_data.get('cover_letter', ''),
            screening_answers=validated_data.get('screening_answers', {}),
        )


class ApplicationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['status']
        read_only_fields = ['shortlisted_at']
