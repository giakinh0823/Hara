from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from Register.models import Profile
from .models import *


# Create your views here.

@login_required
def home_messenger(request, slug):
    list_room = [*MessageRoom.objects.filter(person=request.user) , *MessageRoom.objects.filter(user=request.user)]
    for room in list_room:
        try:
            person = Profile.objects.get(person=room.person)
        except:
            person = Profile.objects.get(user=room.user)
        room.image = person.image
        room.name = person.user.get_full_name()
    profile = Profile.objects.get(user=request.user)
    return render(request, 'Messenger/home_messenger.html',
                  {'list_room': list_room, "profile": profile})


@login_required
def messenger(request, slug):
    try:
        room = MessageRoom.objects.get(slug=slug)
    except:
        personSlug = str(slug)[len(request.user.username):]
        person = User.objects.get(username=personSlug)
        try:
            room = MessageRoom.objects.get(user=request.user, person=person)
        except:
            room = MessageRoom.objects.create(user=request.user, person=person)
            room = room.save()
    list_room = [*MessageRoom.objects.filter(person=request.user) , *MessageRoom.objects.filter(user=request.user)]
    for room in list_room:
        try:
            person = Profile.objects.get(person=room.person)
        except:
            person = Profile.objects.get(user=room.user)
        room.image = person.image
        room.name = person.user.get_full_name()
        room.image = person.image
    messages = Message.objects.filter(room=room)
    profile = Profile.objects.get(user=request.user)
    for message in messages:
        message.is_date = message.created_at.strftime("%M:%S")
    return render(request, 'Messenger/messenger.html',
                  {"room": room, "messages": messages, 'list_room': list_room, "profile": profile})
