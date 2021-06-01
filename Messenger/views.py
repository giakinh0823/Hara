from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from Register.models import Profile
from .models import *


# Create your views here.

@login_required
def home_messenger(request, slug):
    list_room = [*MessageRoom.objects.filter(person=request.user), *MessageRoom.objects.filter(user=request.user)]
    for item in list_room:
        if request.user == item.person:
            person = Profile.objects.get(user=item.user)
        else:
            person = Profile.objects.get(user=item.person)
        item.image = person.image
        item.name = person.user.get_full_name()
    profile = Profile.objects.get(user=request.user)
    return render(request, 'Messenger/home_messenger.html',
                  {'list_room': list_room, "profile": profile})


@login_required
def messenger(request, slug):
    try:
        room = MessageRoom.objects.get(slug=slug)
        print(room)
    except:
        personSlug = str(slug)[len(request.user.username):]
        person = User.objects.get(username=personSlug)
        try:
            try:
                room = MessageRoom.objects.get(user=request.user, person=person)
            except:
                room = MessageRoom.objects.get(user=person, person=request.user)
        except:
            room = MessageRoom.objects.create(user=request.user, person=person)
            room.save()
            room = MessageRoom.objects.get(user=request.user, person=person)
    list_room = [*MessageRoom.objects.filter(person=request.user), *MessageRoom.objects.filter(user=request.user)]
    messages = Message.objects.filter(room=room)
    for item in list_room:
        if request.user == item.person:
            person = Profile.objects.get(user=item.user)
        else:
            person = Profile.objects.get(user=item.person)
        item.image = person.image
        item.name = person.user.get_full_name()
        item.image = person.image

    if request.user == room.person:
        person = Profile.objects.get(user=room.user)
    else:
        person = Profile.objects.get(user=room.person)
    profile = Profile.objects.get(user=request.user)
    for message in messages:
        print(message)
        message.is_date = message.created_at.strftime("%M:%S")
    return render(request, 'Messenger/messenger.html',
                  {"room": room, "messages": messages, 'list_room': list_room, "profile": profile, "person": person})
