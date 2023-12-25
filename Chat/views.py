from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChatMessage, Conversation
from .serializers import ChatMessageSerializer, ConversationSerializer
from .permissions import IsParticipantInConversation
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class ChatMessageListView(APIView):
    permission_classes = [IsParticipantInConversation]

    def get(self, request, format=None):
        chat_messages = ChatMessage.objects.filter(sender=request.user) | ChatMessage.objects.filter(receiver=request.user)
        serializer = ChatMessageSerializer(chat_messages, many=True)
        return Response(serializer.data)



class ConversationListView(APIView):
    permission_classes = [IsParticipantInConversation]

    def get(self, request, format=None):
        conversations = Conversation.objects.filter(team_user = request.user) | Conversation.objects.filter(solo_user=request.user)
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)
