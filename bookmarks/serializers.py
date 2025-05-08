# bookmarks/serializers.py
from rest_framework import serializers
from .models import Bookmark

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['id', 'internship', 'created_at']
        read_only_fields = ['id', 'created_at']
