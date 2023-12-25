from django.urls import path
from . import views

urlpatterns = [
    path('chat-messages/', views.ChatMessageListView.as_view(), name='chatmessage-list-create'),
    path('conversations/', views.ConversationListView.as_view(), name='conversation-list-create'),
]
