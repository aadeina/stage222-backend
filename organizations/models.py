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

# Define the choices for employee ranges
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

# Define the choices for industries
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

    # --- UPDATED: Add choices to city field ---
    city = models.CharField(max_length=100, blank=True, choices=MAURITANIAN_CITIES)
    # --- END UPDATED ---

    # --- UPDATED: Add choices to industry field ---
    # For multiple industries, consider storing as a JSONField if Django version < 3.1
    # or a PostgreSQL ArrayField. For simplicity with CharField, this assumes
    # frontend will send a single selected industry or comma-separated if your custom
    # serializer handles parsing. If only one selection is allowed, CharField with choices is good.
    # If multiple, the serializer validation must ensure all parts are valid choices.
    industry = models.CharField(max_length=255, choices=INDUSTRIES)
    # --- END UPDATED ---

    # --- UPDATED: Add choices to employee_range field ---
    employee_range = models.CharField(max_length=50, blank=True, choices=EMPLOYEE_RANGES)
    # --- END UPDATED ---

    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='organization_logos/', blank=True, null=True)

    license_document = models.FileField(upload_to='org_licenses/', blank=True, null=True)

    social_links = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name