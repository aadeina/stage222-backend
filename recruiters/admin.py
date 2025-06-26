from django.contrib import admin
from .models import RecruiterProfile

@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    def email(self, obj):
        return obj.user.email
    email.short_description = 'Email'

    list_display = (
        'first_name',
        'last_name',
        'email',
        'designation',
        'is_verified',
        'is_onboarded',  # ✅ Added onboarding status
        'organization',
    )
    list_filter = ('is_verified', 'is_onboarded', 'organization')  # ✅ Filter by onboarding
    search_fields = ('first_name', 'last_name', 'user__email')
    ordering = ('-created_at',)
    actions = ['verify_selected', 'unverify_selected']

    def verify_selected(self, request, queryset):
        queryset.update(is_verified=True)
    verify_selected.short_description = "✅ Mark selected recruiters as verified"

    def unverify_selected(self, request, queryset):
        queryset.update(is_verified=False)
    unverify_selected.short_description = "🚫 Mark selected recruiters as unverified"
