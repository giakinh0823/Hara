from django.urls import path
from . import views

app_name = "messenger"

urlpatterns = [
    path('messenger/<slug:slug>/', views.messenger, name="messenger")
]