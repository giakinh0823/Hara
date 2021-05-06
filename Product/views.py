from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from .getdata import data_scrap


# Create your views here.

def getData(request):
    data_scrap(request)
    return HttpResponse('done')


def products(request):
    product = Product.objects.all()
    group_category = GroupCategory.objects.all()
    list_category = Category.objects.all()
    context = {'products': product, 'group_category': group_category, 'category_list': list_category}
    return render(request, 'product/products.html', context)


def productDetail(request):
    pass


def category(request, slug):
    categoryDetail = Category.objects.get(slug=slug)
    product = Product.objects.filter(category=categoryDetail)
    group_category = GroupCategory.objects.all()
    list_category = Category.objects.all()
    context = {
        'category': categoryDetail,
        'products': product,
        'group_category': group_category,
        'category_list': list_category
    }
    return render(request, 'Product/category.html', context)


def groupCategory(request, slug):
    pass
