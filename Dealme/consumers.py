import json
import math
from datetime import datetime
from decimal import Decimal
from time import sleep

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

from Messenger.models import MessageRoom, Message
from Order.models import State, Order
from Product.models import *
from Register.models import *


class ProductsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('connect')
        await self.accept()
        await self.channel_layer.group_add("products", self.channel_name)
        print(f"Add {self.channel_name} channel to products's group")

        @sync_to_async
        def get_products():
            return Product.objects.all()

        for product in await get_products():
            print("Print product")
            await self.send(json.dumps({
                'title': product.title,
                'category': str(product.category.name),
                'price': str(product.price),
                'caption': product.caption,
                'like': product.like,
                'created_at': str(product.created_at),
                'updated_at': str(product.updated_at),
            }))

    async def receive_json(self, message):
        print("receive", message)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("products", self.channel_name)
        print(f"Remove {self.channel_name} channel from products's group")


class CommentsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('connect')
        await self.accept()
        room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_add(room_name, self.channel_name)
        print(f"Add {self.channel_name} channel to comment's group")

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        comment = data['comment']
        username = data['username']
        room = data['room']
        person = data['person']
        avatar = data['avatar']
        name = data['name']

        await self.save_comment(username, room, comment)

        @sync_to_async
        def get_url():
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            return profile.get_absolute_url()

        @sync_to_async
        def get_image():
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            return profile.image.url

        url = await get_url(),
        room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_send(
            room_name,
            {
                'type': 'comment_product',
                'comment': comment,
                'username': username,
                'person': person,
                'avatar': avatar,
                'name': name,
                'url': url,
            }
        )

    async def comment_product(self, event):
        comment = event['comment']
        username = event['username']
        person = event['person']
        avatar = event['avatar']
        url = event['url']
        name = event['name']
        # Gửi tin nhắn tới WebSocket
        await self.send(text_data=json.dumps({
            'comment': comment,
            'username': username,
            'person': person,
            'avatar': avatar,
            'url': url,
            'name': name,
        }))

    async def disconnect(self, close_code):
        room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_discard(room_name, self.channel_name)
        print(f"Remove {self.channel_name} channel from comment's group")

    @sync_to_async
    def save_comment(self, username, room, comment):
        product = Product.objects.get(slug=room)
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user, )
        Comment.objects.create(product=product, user=user, comment=comment, profile=profile)


class NotifierConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('connect')
        await self.accept()
        room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_add(room_name, self.channel_name)
        print(f"Add {self.channel_name} channel to Notifier's group")

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        comment = data['comment']
        username = data['username']
        link = data['link']
        person = data['person']

        await self.save_notify(username, link, comment, person)
        await self.saveSession()
        room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_send(
            room_name,
            {
                'type': 'notification',
                'comment': comment,
                'username': username,
                'link': link,
                'person': person
            }
        )

    @sync_to_async
    def saveSession(self):
        self.scope["session"]["newNotify"] = self.scope["session"]["newNotify"] + 1
        self.scope["session"].save()

    async def notification(self, event):
        comment = event['comment']
        username = event['username']
        person = event['person']
        link = event['link']
        # Gửi tin nhắn tới WebSocket
        await self.send(text_data=json.dumps({
            'comment': comment,
            'username': username,
            'person': person,
            'link': link
        }))

    async def disconnect(self, close_code):
        room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_discard(room_name, self.channel_name)
        print(f"Remove {self.channel_name} channel from Notifier's group")

    @sync_to_async
    def save_notify(self, username, link, comment, person):
        user = User.objects.get(username=username)
        newPerson = User.objects.get(username=person)
        profile = Profile.objects.get(user=newPerson)
        Notifications.objects.create(link=link, content=comment, user=user, new=True, person=newPerson,
                                     profile=profile)


class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('connect')
        await self.accept()
        room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_add(room_name, self.channel_name)
        print(f"Add {self.channel_name} channel to Order's group")

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        name = data['name']
        room = data['room']
        person = data['person']
        state = data['state']
        await self.save_order(room, state, person)
        room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_send(
            room_name,
            {
                'type': 'sendData',
                'name': name,
                'room': room,
                'state': state,
                'person': person
            }
        )

    async def sendData(self, event):
        name = event['name']
        room = event['room']
        state = event['state']
        person = event['person']
        # Gửi tin nhắn tới WebSocket
        await self.send(text_data=json.dumps({
            'name': name,
            'room': room,
            'state': state,
            'person': person
        }))

    async def disconnect(self, close_code):
        room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_discard(room_name, self.channel_name)
        print(f"Remove {self.channel_name} channel from Order's group")

    @sync_to_async
    def save_order(self, room, state, person):
        product = Product.objects.get(slug=room)
        user = User.objects.get(username=product.user)
        state = State.objects.get(slug=state)
        person = User.objects.get(username=person)
        quantity = 1
        price = int(math.ceil(product.price))
        Order.objects.create(product=product, state=state, person=person, quantity=quantity, price=price, user=user)


class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('connect')
        await self.accept()
        room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_add(room_name, self.channel_name)
        print(f"Add {self.channel_name} channel to Message's group")

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        content = data['content']
        room = data['room']
        person = data['person']
        user = data['user']
        now = datetime.now()
        await self.save_message(room, user, person, content)
        room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_send(
            room_name,
            {
                'type': 'sendData',
                'content': content,
                'room': room,
                'user': user,
                'person': person,
                "date": now,
            }
        )

    async def sendData(self, event):
        content = event['content']
        room = event['room']
        user = event['user']
        person = event['person']
        date = event['date']
        # Gửi tin nhắn tới WebSocket
        await self.send(text_data=json.dumps({
            'content': content,
            'room': room,
            'user': user,
            'person': person,
                'date': str(date.strftime("%M:%S")),
        }))

    async def disconnect(self, close_code):
        room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_discard(room_name, self.channel_name)
        print(f"Remove {self.channel_name} channel from Message's group")

    @sync_to_async
    def save_message(self, room, user, person, content):
        roomMessage = MessageRoom.objects.get(slug=room)
        user = User.objects.get(username=user)
        message = Message.objects.create(room=roomMessage, content=content, user=user)
        message.save()
