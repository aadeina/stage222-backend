from django.contrib import admin
from .models import RecruiterProfile

@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'designation', 'is_verified', 'organization')
