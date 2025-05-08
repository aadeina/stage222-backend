from django.db import models
from accounts.models import User
from organizations.models import Organization
from core.models import BaseModel  # Inherit shared fields

class RecruiterProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="recruiter")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    designation = models.CharField(max_length=100)  # e.g., HR Manager
    is_verified = models.BooleanField(default=False)
    
    # ✅ Only ONE recruiter can be linked to ONE organization
    organization = models.OneToOneField(
        Organization,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="recruiter"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.designation}"
