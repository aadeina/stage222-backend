from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'candidate', 'internship', 'status', 'shortlisted', 'created_at']
    list_filter = ['status', 'shortlisted', 'created_at']
    search_fields = ['candidate__user__email', 'internship__title']
