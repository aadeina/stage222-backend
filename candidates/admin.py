from django.contrib import admin
from .models import CandidateProfile

@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'city', 'university', 'graduation_year')
