# organizations/models.py

from django.db import models
import uuid

# Define the choices for cities
MAURITANIAN_CITIES = [
    ("Nouakchott", "Nouakchott"),
    ("Nouadhibou", "Nouadhibou"),
    ("Aïoun", "Aïoun"),
    ("Akjoujt", "Akjoujt"),
    ("Aleg", "Aleg"),
    ("Atar", "Atar"),
    ("Kaédi", "Kaédi"),
    ("Kiffa", "Kiffa"),
    ("Néma", "Néma"),
    ("Rosso", "Rosso"),
    ("Sélibabi", "Sélibabi"),
    ("Tidjikdja", "Tidjikdja"),
    ("Zouerate", "Zouerate"),
]

EMPLOYEE_RANGES = [
    ("0–1", "0–1"),
    ("2–10", "2–10"),
    ("11–50", "11–50"),
    ("51–200", "51–200"),
    ("201–500", "201–500"),
    ("501–1000", "501–1000"),
    ("1001–5000", "1001–5000"),
    ("5000+", "5000+"),
]

INDUSTRIES = [
    ("Advertising/Marketing", "Advertising/Marketing"),
    ("Agriculture/Dairy", "Agriculture/Dairy"),
    ("Animation", "Animation"),
    ("Architecture/Interior Design", "Architecture/Interior Design"),
    ("Automobile", "Automobile"),
    ("BPO", "BPO"),
    ("Biotechnology", "Biotechnology"),
    ("Consulting", "Consulting"),
    ("Data Science/AI", "Data Science/AI"),
    ("Design/UX", "Design/UX"),
    ("E-commerce", "E-commerce"),
    ("Education", "Education"),
    ("Finance", "Finance"),
    ("Government/Public Sector", "Government/Public Sector"),
    ("Healthcare", "Healthcare"),
    ("HR/Recruitment", "HR/Recruitment"),
    ("IT/Software", "IT/Software"),
    ("Legal", "Legal"),
    ("Logistics/Supply Chain", "Logistics/Supply Chain"),
    ("Manufacturing", "Manufacturing"),
    ("Media/Journalism", "Media/Journalism"),
    ("NGO / Non-Profit", "NGO / Non-Profit"),
    ("Retail", "Retail"),
    ("Telecommunications", "Telecommunications"),
    ("Travel & Tourism", "Travel & Tourism"),
    ("Other", "Other"),
]


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)
    is_independent = models.BooleanField(default=False)  # For practitioners

    about = models.TextField(max_length=500, blank=True)
    city = models.CharField(max_length=100, blank=True, choices=MAURITANIAN_CITIES)
    industry = models.CharField(max_length=255, choices=INDUSTRIES)
    employee_range = models.CharField(max_length=50, blank=True, choices=EMPLOYEE_RANGES)

    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='organization_logos/', blank=True, null=True)
    license_document = models.FileField(upload_to='org_licenses/', blank=True, null=True)
    social_links = models.JSONField(blank=True, null=True)

    # ✅ NEW fields for full UI support
    founded_year = models.PositiveIntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
