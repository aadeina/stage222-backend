from rest_framework import serializers
from .models import Internship

class InternshipSerializer(serializers.ModelSerializer):
    recruiter_name = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()
    stipend_display = serializers.SerializerMethodField()
    applicants_count = serializers.SerializerMethodField()  # ✅ Add this line

    class Meta:
        model = Internship
        fields = '__all__'  # This will now include applicants_count too
        read_only_fields = [
            'id',
            'recruiter',
            'organization',
            'created_at',
            'updated_at',
        ]

    def get_recruiter_name(self, obj):
        return obj.recruiter.user.get_full_name()

    def get_organization(self, obj):
        org = obj.organization
        return {
            "id": org.id,
            "name": org.name,
            "logo": org.logo.url if org.logo else None,
            "city": org.city,
            "website": org.website,
        }

    def get_stipend_display(self, obj):
        if obj.stipend_type == 'fixed':
            return f"{obj.fixed_pay_min:,} – {obj.fixed_pay_max:,} MRU"
        elif obj.stipend_type == 'range':
            return f"{obj.fixed_pay_min:,} – {obj.fixed_pay_max:,} MRU (+ Incentives)"
        elif obj.stipend_type == 'unpaid':
            return "Unpaid"
        return "—"

    def get_applicants_count(self, obj):
        return obj.applications.count()  # ✅ Uses related_name from Application model

    def validate(self, data):
        min_fixed = data.get('fixed_pay_min')
        max_fixed = data.get('fixed_pay_max')
        if min_fixed is not None and max_fixed is not None:
            if min_fixed > max_fixed:
                raise serializers.ValidationError("Fixed pay min cannot exceed max")

        min_incentive = data.get('incentives_min')
        max_incentive = data.get('incentives_max')
        if min_incentive is not None and max_incentive is not None:
            if min_incentive > max_incentive:
                raise serializers.ValidationError("Incentives min cannot exceed max")

        return data
