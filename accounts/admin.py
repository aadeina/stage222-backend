from django.contrib import admin
from .models import User, Admin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'is_active', 'is_verified', 'created_at')
    list_filter = ('role', 'is_active', 'is_verified')
    search_fields = ('email',)
    ordering = ('-created_at',)
    actions = ['activate_users', 'deactivate_users']

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
    activate_users.short_description = "✅ Activate selected users"

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_users.short_description = "❌ Deactivate selected users"


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'email')
    search_fields = ('user__email',)





from django.contrib import admin

admin.site.site_header = "Stage222 Admin Dashboard"
admin.site.site_title = "Stage222 Admin"
admin.site.index_title = "Welcome to the Stage222 Admin Control Panel"
