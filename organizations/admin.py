from django.contrib import admin
from .models import Organization
from recruiters.models import RecruiterProfile

class RecruiterInline(admin.TabularInline):
    model = RecruiterProfile
    extra = 0

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'website')
    search_fields = ('name', 'industry')
    ordering = ('name',)
    inlines = [RecruiterInline]
