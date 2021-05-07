from django.shortcuts import render
from Product.models import *
from Register.models import *
# Create your views here.
import random


def home(request):
    products = Product.objects.all()
    ran = random.randint(1, len(products) - 20)
    newNotify = Notifications.objects.filter(new=True)
    request.session['newNotify'] = len(newNotify)
    return render(request, 'Home/home.html', {'newProducts': products[len(products)-20:], 'favoriteProducts':products[0:20], 'randomProduct':products[ran:ran+20]})


#components
def form1(request):
    return render(request, 'components/form-1.html')