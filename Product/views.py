from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from Register.models import Profile
from .models import *

from .getdata import data_scrap

import random


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

    context = {'products': list_product, 'group_category': group_category, 'category_list': list_category}
    return render(request, 'product/products.html', context)


def productDetail(request, slug):
    product_detail = Product.objects.get(slug=slug)
    profile_detail = Profile.objects.get(user=product_detail.user)
    list_products = Product.objects.filter(category=product_detail.category)
    ran = random.randint(0, len(list_products) - 3)
    videos = Video.objects.filter(product=product_detail)
    images = Image.objects.filter(product=product_detail)
    comments = Comment.objects.filter(product=product_detail)
    context = {
        'product_detail': product_detail,
        'profile_detail': profile_detail,
        'list_products': list_products[ran:ran + 3],
        'videos':videos,
        'images':images,
        'comments': comments,
    }
    return render(request, 'product/product_detail.html',context)


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
    context = {'products': product, 'group_category': group_category, 'category_list': list_category,
               'category_group': category_group}
    return render(request, 'Product/group_category.html', context)


def create_product(request):
    return render(request, 'product/create_product.html')
