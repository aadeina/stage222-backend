from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'body', 'internship', 'is_read', 'timestamp']
    list_filter = ['is_read', 'timestamp']
    search_fields = ['sender__email', 'receiver__email', 'body']
    ordering = ['-timestamp']
