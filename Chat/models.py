from django.db import models
from Users.models import TeamUser, SoloUser
from django.db.models.signals import pre_delete
from django.dispatch import receiver

# Create your models here.
class ChatMessage(models.Model):
    sender = models.ForeignKey('Users.CustomUser', on_delete=models.SET_NULL, null=True, related_name='sent_messages')
    receiver = models.ForeignKey('Users.CustomUser', on_delete=models.SET_NULL, null=True, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} to {self.receiver} at {self.timestamp}"


class Conversation(models.Model):
    team_user = models.ForeignKey('Users.TeamUser', on_delete=models.SET_NULL, null=True, related_name='teams_conversations')
    solo_user = models.ForeignKey('Users.SoloUser', on_delete=models.SET_NULL, null=True, related_name='solos_conversations')
    messages = models.ManyToManyField(ChatMessage, related_name='conversation_messages', blank=True)

    def __str__(self):
        return f"Conversation between {self.team_user} and {self.solo_user}"

    def is_participant(self, user):
        return self.team_user == user.team_user if self.team_user else self.solo_user == user.solo_user

@receiver(pre_delete, sender=Conversation)
def delete_chat_messages(sender, instance, **kwargs):
    instance.messages.all().delete()
