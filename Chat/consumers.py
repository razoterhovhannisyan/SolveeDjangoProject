import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connected")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print("WebSocket disconnected")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print("WebSocket received a message:", text_data)

        from .models import ChatMessage, Conversation
        from Users.models import TeamUser, SoloUser


        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            sender_id = text_data_json['sender_id']
            receiver_id = text_data_json['receiver_id']
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return

        await self.save_message(sender_id, receiver_id, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message,
                'sender_id': sender_id,
                'receiver_id': receiver_id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        receiver_id = event['receiver_id']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
            'receiver_id': receiver_id
        }))

    @sync_to_async
    def save_message(self, sender_id, receiver_id, message):

        from .models import ChatMessage, Conversation
        from Users.models import TeamUser, SoloUser


        sender = get_object_or_404(TeamUser, id=sender_id) if TeamUser.objects.filter(id=sender_id).exists() else get_object_or_404(SoloUser, id=sender_id)
        receiver = get_object_or_404(TeamUser, id=receiver_id) if TeamUser.objects.filter(id=receiver_id).exists() else get_object_or_404(SoloUser, id=receiver_id)

        chat_message = ChatMessage.objects.create(sender=sender, receiver=receiver, message=message)

        if sender.user_type == 'Team':
            team_user = sender
            solo_user = receiver
        elif sender.user_type == 'Solo':
            team_user = receiver
            solo_user = sender

        conversation = Conversation.objects.filter(team_user=team_user, solo_user=solo_user).first()

        if not conversation:
            conversation = Conversation.objects.create(team_user=team_user, solo_user=solo_user)
        conversation.messages.add(chat_message)
