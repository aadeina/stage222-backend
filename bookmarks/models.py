from django.db import models
from candidates.models import CandidateProfile
from internships.models import Internship
import uuid

class Bookmark(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='bookmarks')
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['candidate', 'internship']

    def __str__(self):
        return f"{self.candidate.user.email} bookmarked {self.internship.title}"
