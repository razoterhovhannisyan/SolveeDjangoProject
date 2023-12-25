from rest_framework import serializers
from .models import ChatMessage, Conversation
# from Users.serializers import TeamUserSerializer,

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['sender', 'receiver', 'message']


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['team_user', 'solo_user']
