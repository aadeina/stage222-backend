import uuid
from django.db import models
from accounts.models import User
from internships.models import Internship

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    body = models.TextField()
    internship = models.ForeignKey(Internship, null=True, blank=True, on_delete=models.SET_NULL, related_name="related_messages")
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sender.email} ➜ {self.receiver.email} - {self.body[:30]}"
