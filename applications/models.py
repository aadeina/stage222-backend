import uuid
from django.db import models
from django.utils import timezone
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

    # ✅ Shortlist logic
    shortlisted = models.BooleanField(default=False)
    shortlisted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['candidate', 'internship']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.candidate.user.email} → {self.internship.title}"

    def mark_shortlisted(self):
        """Mark the application as shortlisted and timestamp it."""
        self.shortlisted = True
        self.shortlisted_at = timezone.now()
        self.save()
