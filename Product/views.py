import math

import stripe
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from django.views.generic import TemplateView

from Register.models import Profile, Notifications
from .models import *
from django.views import View
from django.conf import settings
from django.http import JsonResponse
from .getdata import data_scrap

import random

stripe.api_key = settings.STRIPE_SECRET_KEY



# Create your views here.

def getData(request):
    data_scrap(request)
    return HttpResponse('done')


def products(request):
    group_category = GroupCategory.objects.all()
    list_category = Category.objects.all()
    list_product = Product.objects.all()
    if request.method == 'GET':
        try:
            getProduct = request.GET['search']
        except:
            getProduct = None
        if getProduct:
            list_product = list_product.filter(Q(title__icontains=request.GET['search']))

    context = {
        'products': list_product,
        'group_category': group_category,
        'category_list': list_category
    }
    if request.user.is_authenticated:
        notify = Notifications.objects.all()
        newNotify = notify.filter(new=True)
        request.session['newNotify'] = len(newNotify)
        newNotify = Notifications.objects.filter(new=True)
        context = {
            'products': list_product,
            'group_category': group_category,
            'category_list': list_category,
            'newNotify': reversed(newNotify),
            'notify': reversed(notify),
        }
    return render(request, 'product/products.html', context)


def productDetail(request, slug):
    product_detail = Product.objects.get(slug=slug)
    profile_detail = Profile.objects.get(user=product_detail.user)
    profile_user = Profile.objects.get(user=request.user)
    list_products = Product.objects.filter(category=product_detail.category)
    ran = random.randint(0, len(list_products) - 3)
    videos = Video.objects.filter(product=product_detail)
    images = Image.objects.filter(product=product_detail)
    comments = Comment.objects.filter(product=product_detail)
    context = {
        'product_detail': product_detail,
        'profile_detail': profile_detail,
        'list_products': list_products[ran:ran + 3],
        'videos': videos,
        'images': images,
        'comments': comments,
        'profile_user': profile_user,
        'STRIPE_SECRET_KEY': settings.STRIPE_SECRET_KEY,
    }
    if request.user.is_authenticated:
        notify = Notifications.objects.all()
        clickNotify = notify.filter(link=product_detail.get_absolute_url())
        for item in clickNotify:
            item.new = False
            item.save()
        newNotify = Notifications.objects.filter(new=True)
        notify = notify[:len(notify) - len(newNotify)]
        request.session['newNotify'] = len(newNotify)
        context = {
            'product_detail': product_detail,
            'profile_detail': profile_detail,
            'list_products': list_products[ran:ran + 3],
            'videos': videos,
            'images': images,
            'comments': comments,
            'profile_user': profile_user,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
            'newNotify': reversed(newNotify),
            'notify': reversed(notify),
        }
    return render(request, 'product/product_detail.html', context)


def category(request, slug):
    categoryDetail = Category.objects.get(slug=slug)
    product = Product.objects.filter(category=categoryDetail)
    group_category = GroupCategory.objects.all()
    list_category = Category.objects.all()
    if request.method == 'GET':
        try:
            getProduct = request.GET['search']
        except:
            getProduct = None
        if getProduct:
            product = product.filter(Q(title__icontains=request.GET['search']))
    context = {
        'category': categoryDetail,
        'products': product,
        'group_category': group_category,
        'category_list': list_category
    }
    if request.user.is_authenticated:
        notify = Notifications.objects.all()
        newNotify = Notifications.objects.filter(new=True)
        request.session['newNotify'] = len(newNotify)
        notify = notify[:len(notify) - len(newNotify)]
        context = {
            'category': categoryDetail,
            'products': product,
            'group_category': group_category,
            'category_list': list_category,
            'newNotify': reversed(newNotify),
            'notify': reversed(notify),
        }
    return render(request, 'Product/category.html', context)


def groupCategory(request, slug):
    group_category = GroupCategory.objects.all()
    list_category = Category.objects.all()
    category_group = group_category.get(slug=slug)
    product = Product.objects.all()
    if request.method == 'GET':
        try:
            getProduct = request.GET['search']
        except:
            getProduct = None
        if getProduct:
            product = product.filter(Q(title__icontains=request.GET['search']))
    context = {
        'products': product,
        'group_category': group_category,
        'category_list': list_category,
        'category_group': category_group,
    }
    if request.user.is_authenticated:
        notify = Notifications.objects.all()
        newNotify = Notifications.objects.filter(new=True)
        request.session['newNotify'] = len(newNotify)
        notify = notify[:len(notify) - len(newNotify)]
        context = {
            'products': product,
            'group_category': group_category,
            'category_list': list_category,
            'category_group': category_group,
            'newNotify': reversed(newNotify),
            'notify': reversed(notify),
        }
    return render(request, 'Product/group_category.html', context)


@login_required
def create_product(request):
    if request.user.is_authenticated:
        notify = Notifications.objects.all()
        newNotify = Notifications.objects.filter(new=True)
        request.session['newNotify'] = len(newNotify)
        notify = notify[:len(notify) - len(newNotify)]
        context = {
            'newNotify': reversed(newNotify),
            'notify': reversed(notify),
        }
    return render(request, 'product/create_product.html')

# 4242 4242 4242 4242
class CreateCheckoutSessionView(View):
    def post(self, request, *args,**kwargs):
        slug = self.kwargs['slug']
        product = Product.objects.get(slug=slug)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(math.ceil(product.price)) * 100,
                        'product_data': {
                            'name': product.title,
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


def success(request):
    return render(request, "order/success.html")

def error(request):
    return render(request, "order/error.html")


def cancel(request):
    return render(request,"order/cancel.html")


