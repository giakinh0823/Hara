from django.urls import path
from . import views

app_name = "messenger"

urlpatterns = [
    path('messenger/<slug:slug>/', views.messenger, name="messenger"),
    path('home_messenger/<slug:slug>/', views.home_messenger, name="home_messenger")
]