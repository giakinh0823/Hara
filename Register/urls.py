from django.urls import path
from . import views



app_name = 'register'

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/<slug:slug>/', views.profile, name='profile'),
    path('profile/<slug:slug>/edit', views.edit_profile, name='edit_profile'),
    path('profile-detail/<slug:slug>/', views.profileDetail, name='profile_detail')
]

