from allauth.account.utils import send_email_confirmation
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.shortcuts import render, redirect

from Product.models import Product
from .forms import SignUpForm, ProfileForm, EditUser

# Create your views here.
from .models import Profile, Notifications


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
            # user = form.save(commit=False)
            # user.is_active = False
            # user.save()
            # send_email_confirmation(request, user, True)
            # return render(request, 'account/verification_sent.html')
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
    if request.method == 'GET':
        try:
            getProduct = request.GET['search']
        except:
            getProduct = None
        if getProduct:
            products = products.filter(Q(title__icontains=request.GET['search']))
    notify = Notifications.objects.filter(user=request.user)
    newNotify = Notifications.objects.filter(new=True, user=request.user)
    request.session['newNotify'] = len(newNotify)
    notify = notify[:len(notify) - len(newNotify)]
    if notify or newNotify:
        request.session['newNotify'] = len(newNotify)
        notify = notify[:len(notify) - len(newNotify)]
        notify = reversed(notify)
        if not newNotify or len(newNotify) == 0:
            newNotify = None
        else:
            newNotify = reversed(newNotify)
    context = {
        'profile': userProfile,
        'products': products,
        'newNotify': newNotify,
        'notify': notify,
    }
    return render(request, 'register/profile.html', context)

@login_required
def edit_profile(request, slug):
    notify = Notifications.objects.filter(user=request.user)
    newNotify = Notifications.objects.filter(user=request.user, new=True)
    request.session['newNotify'] = len(newNotify)
    notify = notify[:len(notify) - len(newNotify)]
    if notify or newNotify:
        request.session['newNotify'] = len(newNotify)
        notify = notify[:len(notify) - len(newNotify)]
        notify = reversed(notify)
        if not newNotify or len(newNotify) == 0:
            newNotify = None
        else:
            newNotify = reversed(newNotify)
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
            return redirect('register:profile', slug=userProfiler.slug)
        else:
            context = {
                'formUser': formUser,
                'formProfile': formProfile,
                'userProfile': userProfile,
                'error': 'Something is wrong',
                'newNotify': newNotify,
                'notify': notify,
            }
            return render(request, 'Register/edit_profile.html', context)
    context = {
        'formUser': formUser,
        'formProfile': formProfile,
        'userProfile': userProfile,
        'newNotify': newNotify,
        'notify': notify,
    }
    return render(request,'Register/edit_profile.html', context)


def profileDetail(request, slug):
    notify = Notifications.objects.filter(user=request.user)
    newNotify = Notifications.objects.filter(new=True, user=request.user)
    request.session['newNotify'] = len(newNotify)
    notify = notify[:len(notify) - len(newNotify)]
    if notify:
        notify = reversed(notify)
    else:
        notify = None
    if not newNotify or len(newNotify) == 0:
        newNotify = None
    else:
        newNotify = reversed(newNotify)
    context = {
        'newNotify': newNotify,
        'notify':notify ,
    }
    pass