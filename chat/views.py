# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.models import User
from .models import ChatRoom, Message
from property.models import PropertyPost
from .forms import MessageForm

@login_required
def user_chat_rooms(request):
    user = request.user
    chat_rooms = ChatRoom.objects.filter(Q(user1=user) | Q(user2=user)).order_by('-updated_at')

    users_in_rooms = []
    for room in chat_rooms:
        if room.user1 == user:
            recipient = room.user2
        else:
            recipient = room.user1
        users_in_rooms.append((room, recipient))
    

    context = {
        'chat_rooms_with_users': users_in_rooms,
        'title': "Messages"
    }
    
    return render(request, 'chat/chat_rooms.html', context)


@login_required
def chat_room_messages(request, recipient_id, property_id=None):
    user = request.user
    recipient = get_object_or_404(User, id=recipient_id)

    # Check if a ChatRoom already exists between the two users
    chat_room = ChatRoom.objects.filter(
        Q(user1=user, user2=recipient) | Q(user1=recipient, user2=user)
    ).first()

    if not chat_room:
        # If a ChatRoom does not exist, create one with defaults
        chat_room = ChatRoom.objects.create(user1=user, user2=recipient)

    try:
        unread_message = Message.objects.filter(sent_to=request.user, chat_room=chat_room, read=False)
        for chat in unread_message:
            chat.read = True
            chat.save()
    except Exception:
        pass
    messages = Message.objects.filter(chat_room=chat_room).order_by('id')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sent_from = user
            message.sent_to = recipient
            if property_id:
                message.property_id = property_id  

            chat_room.last_message = form.cleaned_data.get('message')
            chat_room.updated_at = timezone.now()
            chat_room.save()
            message.chat_room = chat_room

            message.save()
            form = MessageForm()
    else:
        form = MessageForm()

    context = {
        'roommessage': messages,
        'form': form,
        'recipient': recipient,
        'property_id': property_id,
        'curr_user': request.user,
        'title': 'Chat'
    }
    
    return render(request, 'chat/messages.html', context)
