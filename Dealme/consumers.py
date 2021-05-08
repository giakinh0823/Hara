import json
from decimal import Decimal
from time import sleep

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

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
        profile = Profile.objects.get(user=user,)
        Comment.objects.create(product=product, user=user, comment=comment, profile=profile)


class NotifierConsumer(AsyncWebsocketConsumer):
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
        product = data['product']
        person = data['person']

        await self.save_notify(username, product, comment, person)
        await self.saveSession()
        room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_send(
            room_name,
            {
                'type': 'notification',
                'comment': comment,
                'username': username,
                'product': product,
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
        product = event['product']
        person = event['person']
        # Gửi tin nhắn tới WebSocket
        await self.send(text_data=json.dumps({
            'comment': comment,
            'username': username,
            'product': product,
            'person': person
        }))

    async def disconnect(self, close_code):
        room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_discard(room_name, self.channel_name)
        print(f"Remove {self.channel_name} channel from comment's group")

    @sync_to_async
    def save_notify(self, username, product, comment, person):
        user = User.objects.get(username=username)
        newPerson = User.objects.get(username = person)
        profile = Profile.objects.get(user = newPerson)
        Notifications.objects.create(link=product, content=comment, user=user, new=True, person=newPerson, profile=profile)
