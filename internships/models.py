# internships/models.py
from django.db import models
from core.models import BaseModel
import uuid

class Internship(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # 🎯 Basic Info
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=100)
    opportunity_type = models.CharField(
        max_length=20,
        choices=[('job', 'Job'), ('internship', 'Internship')],
        default='internship'
    )
    job_type = models.CharField(
        max_length=20,
        choices=[('full-time', 'Full-time'), ('part-time', 'Part-time')],
        blank=True,
        null=True
    )
    type = models.CharField(
        max_length=20,
        choices=[('remote', 'Remote'), ('hybrid', 'Hybrid'), ('in-office', 'In-office')],
        default='remote'
    )

    # ⏳ Duration & Timing
    duration = models.CharField(max_length=50)
    duration_weeks = models.PositiveIntegerField()
    start_date = models.DateField()
    deadline = models.DateField()

    # 💰 Compensation
    stipend_type = models.CharField(
        max_length=20,
        choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')],
        default='paid'
    )
    stipend = models.DecimalField(max_digits=8, decimal_places=2)
    fixed_pay_min = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    fixed_pay_max = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    incentives_min = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    incentives_max = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    # 📦 Extras
    perks = models.JSONField(default=list, blank=True)
    responsibilities = models.TextField(blank=True)
    preferences = models.JSONField(default=list, blank=True)
    screening_questions = models.JSONField(default=list, blank=True)
    alternate_phone = models.CharField(max_length=20, blank=True, null=True)

    # 📌 Other Metadata
    openings = models.PositiveIntegerField()
    status = models.CharField(
        max_length=10,
        choices=[('open', 'Open'), ('closed', 'Closed')],
        default='open'
    )
    approval_status = models.CharField(
        max_length=10,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    rejection_reason = models.TextField(null=True, blank=True)

    # 🔗 Foreign Keys
    recruiter = models.ForeignKey(
        'recruiters.RecruiterProfile',
        on_delete=models.CASCADE,
        related_name='internships'
    )
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='internships'
    )

    def __str__(self):
        return self.title
