from django.contrib import admin
from .models import Internship

@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'recruiter', 'status', 'deadline')
    search_fields = ('title', 'description')
    list_filter = ('status', 'location')
