from django.urls import path
from .views import SendMessageView, MessageThreadView, MarkMessageReadView, InboxView

urlpatterns = [
    path('send/', SendMessageView.as_view(), name='message-send'),
    path('with/<uuid:user_id>/', MessageThreadView.as_view(), name='message-thread'),
    path('<uuid:pk>/read/', MarkMessageReadView.as_view(), name='message-mark-read'),
    path('inbox/', InboxView.as_view(), name='message-inbox'),
]
