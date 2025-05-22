from django.db import models
from accounts.models import User
from organizations.models import Organization
from core.models import BaseModel
from django.core.exceptions import ValidationError

class RecruiterProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="recruiter")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        blank=False,
        help_text="Phone number must start with 2, 3, or 4 and be 8 digits long"
    )
    designation = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)

    organization = models.OneToOneField(
        Organization,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="recruiter"
    )

    def clean(self):
        if not self.phone or not self.phone.startswith(('2', '3', '4')) or len(self.phone) != 8:
            raise ValidationError("Phone number must start with 2, 3, or 4 and be 8 digits long.")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.designation}"
