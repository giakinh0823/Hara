from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from Product.models import Product

@login_required
def order(request, slug):
    product_detail = Product.objects.get(slug=slug)
    context = {
        'product_detail': product_detail,
    }
    return render(request, 'order/order.html',context)