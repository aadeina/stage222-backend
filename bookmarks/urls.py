from django.urls import path
from .views import (
    BookmarkListCreateToggleView,
    BookmarkDeleteView,
    BookmarkCountView
)

urlpatterns = [
    # 📋 List all bookmarks (with count)
    path('', BookmarkListCreateToggleView.as_view(), name='bookmark-list'),

    # 🔄 Toggle bookmark (add/remove)
    path('<uuid:internship_id>/', BookmarkListCreateToggleView.as_view(), name='bookmark-toggle'),

    # ❌ Delete specific bookmark by ID
    path('<uuid:id>/delete/', BookmarkDeleteView.as_view(), name='bookmark-delete'),

    # 🔢 Get only the count of bookmarks
    path('count/', BookmarkCountView.as_view(), name='bookmark-count'),
]
