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
        await self.channel_layer.group_discard("users", self.channel_name)
        print(f"Remove {self.channel_name} channel from products's group")

