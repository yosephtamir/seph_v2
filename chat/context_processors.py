'''Used to handle unread messages of a user'''
from .models import Message

def unread_messages(request):
    if request.user.is_authenticated:
        unread_message_count = Message.objects.filter(sent_to=request.user, read=False).count()
        return {'unread_message_count': unread_message_count}
    return {'unread_message_count': 0}
