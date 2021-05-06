from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from Product.models import Product
from .forms import SignUpForm, ProfileForm, EditUser

# Create your views here.
from .models import Profile


@user_passes_test(lambda u: u.is_anonymous, login_url='home:home')
def loginUser(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'register/login.html',
                          {'form': AuthenticationForm(), 'error': "Username or Password wrong"})
        else:
            login(request, user)
            return redirect('home:home')
    return render(request, 'register/login.html', {'form': AuthenticationForm()})


@login_required
def logoutUser(request):
    logout(request)
    return redirect('home:home')


@user_passes_test(lambda u: u.is_anonymous, login_url='home:home')
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid() and form.cleaned_data.get('password1') == form.cleaned_data.get('password2'):
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home:home')
        else:
            return render(request, 'register/signup.html', {'form': form, 'error': 'Username or Email have been create !!!'})
    else:
        form = SignUpForm()
        return render(request, 'register/signup.html', {'form': form})

@login_required
def profile(request, slug):
    try:
        userProfile = Profile.objects.get(user=request.user)
    except:
        userProfile = None
    products = Product.objects.filter(user=request.user)
    return render(request, 'register/profile.html', {'profile': userProfile, 'products': products})

@login_required
def edit_profile(request, slug):
    try:
        userProfile = Profile.objects.get(user=request.user)
    except:
        userProfile = None
    formUser = EditUser(instance=request.user)
    formProfile = ProfileForm(instance=userProfile)
    if request.method == 'POST':
        formUser = EditUser(request.POST, instance=request.user)
        formProfile = ProfileForm(request.POST, instance=userProfile)
        if formProfile.is_valid() and formUser.is_valid():
            userProfiler = formProfile.save(commit=False)
            user = formUser.save(commit=False)
            userProfiler.user = request.user
            if 'image' in request.FILES:
                userProfiler.image = request.FILES['image']
            userProfiler.save()
            user.save()
            return redirect(userProfile.get_absolute_url())
        else:
            context = {'formUser': formUser, 'formProfile': formProfile,'userProfile': userProfile ,'error': 'Something is wrong'}
            return render(request, 'Register/edit_profile.html', context)
    return render(request,'Register/edit_profile.html', {'formUser': formUser,'formProfile': formProfile, 'userProfile': userProfile })
