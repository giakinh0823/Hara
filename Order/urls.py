from django.urls import path
from . import views


app_name = 'order'

urlpatterns = [
    path('order/<slug:slug>/', views.order, name='order')
]