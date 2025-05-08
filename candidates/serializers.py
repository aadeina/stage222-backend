import re
from rest_framework import serializers
from .models import CandidateProfile, Skill

# 🧠 Skill serializer (used in nested read/write)
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']


# 👤 Candidate profile serializer
class CandidateSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = CandidateProfile
        fields = "__all__"
        read_only_fields = ["user", "resume"]

    def validate_phone(self, value):
        pattern = r'^\+222(2|3|4)\d{7}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Phone must be a valid Mauritanian number starting with +2222, +2223, or +2224."
            )
        return value

    def validate_resume(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Resume file too large (max 2MB).")
        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError("Resume must be a PDF.")
        return value

class CandidateSkillUpdateSerializer(serializers.ModelSerializer):
    skills = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Skill.objects.all()
    )

    class Meta:
        model = CandidateProfile
        fields = ['skills']
