from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from Register.models import Profile
from .models import *


# Create your views here.


@login_required
def messenger(request, slug):
    room = MessageRoom.objects.get(slug=slug)
    list_room = MessageRoom.objects.filter(user = request.user)
    for room in list_room:
        person = Profile.objects.get(user = room.person)
        room.image = person.image
    messages = Message.objects.filter(room=room)
    profile = Profile.objects.get(user=request.user)
    for message in messages:
        message.is_date = message.created_at.strftime("%M:%S")
    return render(request, 'Messenger/messenger.html', {"room": room, "messages": messages, 'list_room': list_room, "profile": profile})


def create_room_message(request, slug):
    try:
        message = Message.objects.get(slug=slug)
    except:
        personSlug = str(slug)[len(request.user.username):]
        person = User.objects.get(username=personSlug)
        room = MessageRoom.objects.create(user=request.user, person=person)
        room.save()
    pass
