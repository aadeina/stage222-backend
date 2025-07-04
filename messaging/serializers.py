from rest_framework import serializers
from .models import Message
from internships.models import Internship

class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email', read_only=True)
    receiver_email = serializers.EmailField(source='receiver.email', read_only=True)
    internship_title = serializers.CharField(source='internship.title', read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'receiver',
            'sender_email',
            'receiver_email',
            'body',
            'internship',
            'internship_title',
            'is_read',
            'timestamp'
        ]
        read_only_fields = ['sender', 'is_read', 'timestamp']

    def create(self, validated_data):
        # Set the sender from the request context
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)
