from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from property.models import PropertyPost


class ChatRoom(models.Model):
    """A chatroom representation"""
    last_message = models.CharField(max_length=128, null=True, blank=True)
    user1 = models.ForeignKey(User, related_name='chatrooms_as_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='chatrooms_as_user2', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True) #can not be modified

    def __str__(self):
        return f"ChatRoom between {self.user1.username} and {self.user2.username}"

class Message(models.Model):
    """A message representation"""
    message = models.TextField(max_length=1000)
    read = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    property = models.ForeignKey(PropertyPost,default=None, null=True, on_delete=models.SET_NULL)
    sent_to = models.ForeignKey(User, related_name='messages_received', on_delete=models.CASCADE)
    sent_from = models.ForeignKey(User, related_name='messages_sent', on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True) #can not be modified

    def __str__(self):
        return f"Message from {self.sent_from.username} to {self.sent_to.username}"
