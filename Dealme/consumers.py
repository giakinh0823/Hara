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

        await self.save_comment(username, room, comment)

        @sync_to_async
        def get_image():
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            return profile.image.url

        room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_send(
            room_name,
            {
                'type': 'comment_product',
                'comment': comment,
                'username': username,
                'person': person,
                'avatar': avatar,
            }
        )

    async def comment_product(self, event):
        comment = event['comment']
        username = event['username']
        person = event['person']
        avatar = event['avatar']
        # Gửi tin nhắn tới WebSocket
        await self.send(text_data=json.dumps({
            'comment': comment,
            'username': username,
            'person': person,
            'avatar': avatar,
        }))

    async def disconnect(self, close_code):
        room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_discard(room_name, self.channel_name)
        print(f"Remove {self.channel_name} channel from comment's group")

    @sync_to_async
    def save_comment(self, username, room, comment):
        product = Product.objects.get(slug=room)
        user = User.objects.get(username=username)
        Comment.objects.create(product=product, user=user, comment=comment)


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

        await self.save_notify(username, product, comment)
        await self.saveSession()
        room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_send(
            room_name,
            {
                'type': 'notification',
                'comment': comment,
                'username': username,
                'product': product
            }
        )

    @sync_to_async
    def saveSession(self):
        self.scope["session"].save()
        self.scope["session"]["newNotify"] = self.scope["session"]["newNotify"] + 1


    async def notification(self, event):
        comment = event['comment']
        username = event['username']
        product = event['product']
        # Gửi tin nhắn tới WebSocket
        await self.send(text_data=json.dumps({
            'comment': comment,
            'username': username,
            'product': product,
        }))

    async def disconnect(self, close_code):
        room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_discard(room_name, self.channel_name)
        print(f"Remove {self.channel_name} channel from comment's group")

    @sync_to_async
    def save_notify(self, username, product, comment):
        user = User.objects.get(username=username)
        Notifications.objects.create(link=product, content=comment, user=user, new=True)
