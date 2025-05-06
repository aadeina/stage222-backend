from django.db import models
from django.conf import settings
from core.models import BaseModel  # Shared timestamp base model

def resume_upload_path(instance, filename):
    return f"resumes/{instance.user.id}/{filename}"

class CandidateProfile(BaseModel):  # created_at, updated_at inherited
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="candidate"
    )
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone = models.CharField(
        max_length=12,  # "+222" + 8 digits
        validators=[],
        help_text="Must be a valid Mauritanian number: +2222, +2223, or +2224 prefix"
    )
    city = models.CharField(max_length=100, blank=True, null=True)
    university = models.CharField(max_length=150, blank=True, null=True)
    graduation_year = models.PositiveIntegerField(blank=True, null=True)
    degree = models.CharField(max_length=100, blank=True, null=True)
    resume = models.FileField(upload_to=resume_upload_path, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.email})"
