# internships/models.py
from django.db import models
from core.models import BaseModel
import uuid

class Internship(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=100)
    openings = models.PositiveIntegerField()
    start_date = models.DateField()
    duration_weeks = models.PositiveIntegerField()
    stipend = models.DecimalField(max_digits=8, decimal_places=2)
    deadline = models.DateField()
    status = models.CharField(max_length=10, choices=[('open', 'Open'), ('closed', 'Closed')], default='open')
    
    recruiter = models.ForeignKey('recruiters.RecruiterProfile', on_delete=models.CASCADE, related_name='internships')
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='internships')

    def __str__(self):
        return self.title
