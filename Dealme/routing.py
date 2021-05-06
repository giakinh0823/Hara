from django.urls import path

from Dealme import consumers

ws_urlpatterns = [
    path('ws/products/', consumers.ProductsConsumer.as_asgi()),
]