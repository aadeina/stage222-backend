# internships/admin.py
from django.contrib import admin
from .models import Internship

@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    """✅ Admin panel customization for managing internship listings."""

    list_display = (
        'title', 'recruiter', 'organization', 'location',
        'status', 'approval_status', 'start_date', 'deadline'
    )
    list_filter = ('status', 'approval_status', 'location', 'organization')
    search_fields = (
        'title', 'description',
        'recruiter__user__email', 'organization__name'
    )
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    date_hierarchy = 'start_date'
    list_per_page = 25

    actions = ['mark_as_hidden', 'mark_as_open', 'mark_as_closed']

    def mark_as_hidden(self, request, queryset):
        updated = queryset.update(status='hidden')
        self.message_user(request, f"{updated} internships marked as Hidden.")
    mark_as_hidden.short_description = "🚫 Mark selected internships as Hidden"

    def mark_as_open(self, request, queryset):
        updated = queryset.update(status='open')
        self.message_user(request, f"{updated} internships marked as Open.")
    mark_as_open.short_description = "✅ Mark selected internships as Open"

    def mark_as_closed(self, request, queryset):
        updated = queryset.update(status='closed')
        self.message_user(request, f"{updated} internships marked as Closed.")
    mark_as_closed.short_description = "📦 Mark selected internships as Closed"
