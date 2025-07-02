# adminpanel/serializers.py

from rest_framework import serializers
from accounts.models import User
from recruiters.models import RecruiterProfile
from candidates.models import CandidateProfile

class FullUserSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'is_verified', 'is_active', 'created_at', 'first_name', 'last_name', 'profile']

    def get_first_name(self, obj):
        return obj.first_name or (obj.recruiterprofile.first_name if hasattr(obj, 'recruiterprofile') else None)

    def get_last_name(self, obj):
        return obj.last_name or (obj.recruiterprofile.last_name if hasattr(obj, 'recruiterprofile') else None)

    def get_profile(self, obj):
        if obj.role == 'recruiter' and hasattr(obj, 'recruiterprofile'):
            return {
                "first_name": obj.recruiterprofile.first_name,
                "last_name": obj.recruiterprofile.last_name,
                "phone": obj.recruiterprofile.phone
            }
        if obj.role == 'candidate' and hasattr(obj, 'candidate'):
            return {
                "resume_url": obj.candidate.resume.url if obj.candidate.resume else None,
                "skills": [skill.name for skill in obj.candidate.skills.all()]
            }
        return {}
