from django.contrib import admin
from .models import Internship

@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    """Admin panel customization for managing internship postings."""
    
    list_display = (
        'title', 'recruiter', 'organization', 'location',
        'status', 'start_date', 'deadline'
    )
    list_filter = ('status', 'location', 'organization')
    search_fields = (
        'title', 'description', 'recruiter__user__email', 'organization__name'
    )
    ordering = ('-created_at',)
    actions = ['mark_as_hidden', 'mark_as_open', 'mark_as_closed']

    def mark_as_hidden(self, request, queryset):
        queryset.update(status='hidden')
    mark_as_hidden.short_description = "🚫 Mark selected internships as Hidden"

    def mark_as_open(self, request, queryset):
        queryset.update(status='open')
    mark_as_open.short_description = "✅ Mark selected internships as Open"

    def mark_as_closed(self, request, queryset):
        queryset.update(status='closed')
    mark_as_closed.short_description = "📦 Mark selected internships as Closed"
