from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from core.models import BaseModel  # Shared timestamp base model


def resume_upload_path(instance, filename):
    return f"resumes/{instance.user.id}/{filename}"


# 🧠 Skill model to represent tags like "Python", "React", etc.
class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# 🏙️ Mauritanian cities
MAURITANIAN_CITIES = [
    ('Nouakchott', 'Nouakchott'),
    ('Nouadhibou', 'Nouadhibou'),
    ('Zouerate', 'Zouerate'),
    ('Rosso', 'Rosso'),
    ('Kiffa', 'Kiffa'),
    ('Atar', 'Atar'),
    ('Aleg', 'Aleg'),
    ('Tidjikja', 'Tidjikja'),
    ('Kaedi', 'Kaédi'),
    ('Néma', 'Néma'),
    ('Selibaby', 'Sélibaby'),
]


class CandidateProfile(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="candidate"
    )

    # 👤 Personal Info
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone = models.CharField(
        max_length=12,
        validators=[
            RegexValidator(
                regex=r'^\+222[234]\d{7}$',
                message="Enter a valid Mauritanian number starting with +2222, +2223, or +2224."
            )
        ],
        help_text="Must be a valid Mauritanian number: +2222, +2223, or +2224 prefix"
    )

    # 📍 Location
    city = models.CharField(
        max_length=100,
        choices=MAURITANIAN_CITIES,
        blank=True,
        null=True
    )

    # 🎓 Education
    university = models.CharField(max_length=150, blank=True, null=True)
    graduation_year = models.PositiveIntegerField(blank=True, null=True)
    degree = models.CharField(max_length=100, blank=True, null=True)

    # 📁 Files
    resume = models.FileField(upload_to=resume_upload_path, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    # 🧠 Skills
    skills = models.ManyToManyField(Skill, blank=True, related_name="candidates")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.email})"
