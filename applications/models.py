import uuid
from django.db import models
from candidates.models import CandidateProfile
from internships.models import Internship

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='applications')
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shortlisted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['candidate', 'internship']
        ordering = ['-created_at']  # Optional: newest applications first

    def __str__(self):
        return f"{self.candidate.user.email} → {self.internship.title}"
