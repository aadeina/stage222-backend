from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'candidate',
        'internship',
        'status',
        'is_shortlisted',  # Custom method
        'created_at',
    ]
    list_filter = [
        'status',
        'created_at',
    ]
    search_fields = [
        'candidate__user__email',
        'internship__title',
    ]
    ordering = ['-created_at']

    @admin.display(boolean=True, description='Shortlisted')
    def is_shortlisted(self, obj):
        return obj.status == 'shortlisted'
