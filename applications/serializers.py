from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            'id',
            'cover_letter',
            'status',
            'shortlisted',
            'created_at'
        ]
        read_only_fields = [
            'id',
            'status',
            'shortlisted',
            'created_at'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        internship_id = self.context['view'].kwargs.get("id")
        validated_data['candidate'] = user.candidate
        validated_data['internship_id'] = internship_id
        return super().create(validated_data)

class ApplicationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['status', 'shortlisted']
