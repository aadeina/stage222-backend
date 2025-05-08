# bookmarks/views.py
from rest_framework import generics, permissions
from .models import Bookmark
from .serializers import BookmarkSerializer
from accounts.permissions import IsCandidate

class BookmarkListCreateView(generics.ListCreateAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated, IsCandidate]

    def get_queryset(self):
        return Bookmark.objects.filter(candidate=self.request.user.candidate)

    def perform_create(self, serializer):
        serializer.save(candidate=self.request.user.candidate)

class BookmarkDeleteView(generics.DestroyAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated, IsCandidate]
    lookup_field = 'id'

    def get_queryset(self):
        return Bookmark.objects.filter(candidate=self.request.user.candidate)
