from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from .models import Message
from .serializers import MessageSerializer
from django.contrib.auth import get_user_model
from accounts.permissions import IsRecruiter 

User = get_user_model()

# 💬 Send a new message
class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def perform_create(self, serializer):
        sender = self.request.user
        receiver = serializer.validated_data.get('receiver')
        internship = serializer.validated_data.get('internship', None)

        if receiver.role != 'candidate':
            raise ValidationError("You can only message candidates.")

        if receiver == sender:
            raise ValidationError("You cannot message yourself.")

        serializer.save(sender=sender, internship=internship)


# 🧵 Get all messages with a specific user
class MessageThreadView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        other_user_id = self.kwargs["user_id"]
        return Message.objects.filter(
            Q(sender=user, receiver__id=other_user_id) |
            Q(sender__id=other_user_id, receiver=user)
        ).order_by("timestamp")


# ✅ Mark a message as read
class MarkMessageReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            message = Message.objects.get(pk=pk, receiver=request.user)
            message.is_read = True
            message.save()
            return Response({"detail": "✅ Message marked as read."})
        except Message.DoesNotExist:
            return Response({"detail": "❌ Message not found or unauthorized."}, status=404)
