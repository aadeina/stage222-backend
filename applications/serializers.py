from rest_framework import serializers
from .models import Application
from internships.models import Internship

class ApplicationSerializer(serializers.ModelSerializer):
    screening_answers = serializers.JSONField(required=False)

    # 🧑‍💼 Candidate info for recruiter view
    candidate_name = serializers.CharField(source='candidate.user.get_full_name', read_only=True)
    candidate_email = serializers.EmailField(source='candidate.user.email', read_only=True)
    candidate_resume = serializers.FileField(source='candidate.resume', read_only=True)
    candidate_photo = serializers.ImageField(source='candidate.profile_picture', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id',
            'cover_letter',
            'screening_answers',
            'status',
            'shortlisted_at',
            'created_at',
            # 🧠 Extra recruiter-facing fields:
            'candidate_name',
            'candidate_email',
            'candidate_resume',
            'candidate_photo',
        ]
        read_only_fields = [
            'id',
            'status',
            'shortlisted_at',
            'created_at',
            'candidate_name',
            'candidate_email',
            'candidate_resume',
            'candidate_photo',
        ]

    def validate(self, attrs):
        user = self.context['request'].user
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
