from django.contrib import admin
from .models import User, Admin, EmailOTP, OTPAttempt

# ==============================
# 🔐 User Model Admin
# ==============================

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


# ==============================
# 👤 Admin Profile Admin
# ==============================

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'email')
    search_fields = ('user__email',)


# ==============================
# 🔐 OTP Admin (for email verification)
# ==============================

@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp_code', 'is_used', 'created_at')
    list_filter = ('is_used',)
    search_fields = ('user__email', 'otp_code')
    ordering = ('-created_at',)


# ==============================
# 📊 OTP Attempt Logs
# ==============================

@admin.register(OTPAttempt)
class OTPAttemptAdmin(admin.ModelAdmin):
    list_display = ('email', 'otp_code', 'is_successful', 'ip_address', 'timestamp')
    list_filter = ('is_successful',)
    search_fields = ('email', 'otp_code', 'ip_address')
    ordering = ('-timestamp',)


# ==============================
# 🧠 Admin Site Branding
# ==============================

admin.site.site_header = "Stage222 Admin Dashboard"
admin.site.site_title = "Stage222 Admin"
admin.site.index_title = "Welcome to the Stage222 Admin Control Panel"
