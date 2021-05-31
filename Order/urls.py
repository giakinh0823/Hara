from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('order/', views.order, name='order'),
    path('invest/', views.invest, name='invest'),
    path('order/active/', views.active_order, name='active_order'),
    path('order/success/', views.success_order, name='active_order'),
    path('order/cancel/', views.cancel_order, name='cancel_order'),
    path('order/accept/', views.accept_order, name='accept_order'),
    path('order/complain/<slug:slug>/', views.complain, name='complain'),
]
