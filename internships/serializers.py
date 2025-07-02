from rest_framework import serializers
from .models import Internship

class InternshipSerializer(serializers.ModelSerializer):
    recruiter_name = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()
    stipend_display = serializers.SerializerMethodField()
    applicants_count = serializers.SerializerMethodField()

    class Meta:
        model = Internship
        fields = '__all__'
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
        if obj.stipend_type == 'paid':
            if obj.negotiable:
                return "Negotiable"
            if obj.stipend:
                return f"{obj.stipend:,.0f} MRU"
            return "Paid"
        elif obj.stipend_type == 'unpaid':
            return "Unpaid"
        return "—"

    def get_applicants_count(self, obj):
        return obj.applications.count()

    def validate(self, data):
        stipend_type = data.get('stipend_type')
        negotiable = data.get('negotiable', False)
        stipend = data.get('stipend')

        if stipend_type == 'paid':
            if not negotiable and stipend is None:
                raise serializers.ValidationError({
                    "stipend": "Stipend is required unless negotiable is true."
                })
            if stipend is not None and stipend < 0:
                raise serializers.ValidationError({
                    "stipend": "Stipend must be a positive amount."
                })

        elif stipend_type == 'unpaid':
            # Unpaid internships should not carry stipend or negotiability
            data['stipend'] = None
            data['negotiable'] = False

        return data
