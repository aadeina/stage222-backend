from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Bookmark
from .serializers import BookmarkSerializer
from internships.models import Internship
from accounts.permissions import IsCandidate


class BookmarkListCreateToggleView(APIView):
    """
    GET: List all bookmarks for the authenticated candidate with count.
    POST: Toggle bookmark (add if not exists, remove if already exists).
    """
    permission_classes = [permissions.IsAuthenticated, IsCandidate]

    def get(self, request):
        candidate = request.user.candidate
        bookmarks = Bookmark.objects.filter(candidate=candidate)
        serializer = BookmarkSerializer(bookmarks, many=True)
        return Response({
            "count": bookmarks.count(),
            "results": serializer.data
        })

    def post(self, request, internship_id):
        candidate = request.user.candidate
        try:
            internship = Internship.objects.get(id=internship_id)
        except Internship.DoesNotExist:
            return Response({"detail": "Internship not found."}, status=status.HTTP_404_NOT_FOUND)

        bookmark, created = Bookmark.objects.get_or_create(candidate=candidate, internship=internship)

        if not created:
            bookmark.delete()
            return Response({"detail": "Bookmark removed.", "bookmarked": False}, status=status.HTTP_200_OK)

        return Response({"detail": "Bookmark added.", "bookmarked": True}, status=status.HTTP_201_CREATED)


class BookmarkDeleteView(generics.DestroyAPIView):
    """
    DELETE: Remove a specific bookmark by its UUID.
    """
    permission_classes = [permissions.IsAuthenticated, IsCandidate]
    serializer_class = BookmarkSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Bookmark.objects.filter(candidate=self.request.user.candidate)


class BookmarkCountView(APIView):
    """
    GET: Return only the total count of bookmarks for the candidate.
    """
    permission_classes = [permissions.IsAuthenticated, IsCandidate]

    def get(self, request):
        count = Bookmark.objects.filter(candidate=request.user.candidate).count()
        return Response({"count": count})
