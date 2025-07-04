from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from django.contrib.auth import get_user_model

from accounts.permissions import IsRecruiter
from applications.models import Application
from internships.models import Internship
from .models import Message
from .serializers import MessageSerializer
from applications.serializers import ApplicationUpdateSerializer

User = get_user_model()


# ✉️ Recruiter can send message to any candidate freely
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

        # ✅ No shortlist check anymore
        serializer.save(sender=sender, internship=internship)


# ✅ Automatically notify candidate when accepted
class ApplicationUpdateView(generics.UpdateAPIView):
    serializer_class = ApplicationUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]
    lookup_field = 'id'

    def get_queryset(self):
        return Application.objects.filter(internship__recruiter=self.request.user.recruiter)

    def perform_update(self, serializer):
        application = serializer.save()

        if application.status == 'accepted':
            Message.objects.create(
                sender=self.request.user,
                receiver=application.candidate.user,
                internship=application.internship,
                body=f"🎉 Congratulations! You have been accepted for the internship: {application.internship.title} at {application.internship.organization.name}."
            )


# 🧵 Get all messages with a specific user
class MessageThreadView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        other_user_id = self.kwargs['user_id']
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


# 📬 Inbox: latest message per conversation partner
class InboxView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        all_messages = Message.objects.filter(Q(sender=user) | Q(receiver=user))
        latest_messages = []
        partners_seen = set()

        for msg in all_messages.order_by('-timestamp'):
            partner = msg.receiver if msg.sender == user else msg.sender
            if partner.id not in partners_seen:
                latest_messages.append({
                    'user_id': str(partner.id),
                    'user_email': partner.email,
                    'message': msg.body,
                    'timestamp': msg.timestamp,
                    'is_read': msg.is_read if msg.receiver == user else True,
                    'internship_title': msg.internship.title if msg.internship else None,
                })
                partners_seen.add(partner.id)

        return Response(latest_messages)
