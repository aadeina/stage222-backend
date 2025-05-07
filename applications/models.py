from django.db import models
from accounts.models import User
from internships.models import Internship
from candidates.models import CandidateProfile

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    is_shortlisted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('candidate', 'internship')  # Prevent duplicate applications

    def __str__(self):
        return f"{self.candidate} - {self.internship.title}"
