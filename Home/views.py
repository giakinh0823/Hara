from django.shortcuts import render
from Product.models import *
from Register.models import *
# Create your views here.
import random


def home(request):
    products = Product.objects.all()
    ran = random.randint(1, len(products) - 20)
    notify = Notifications.objects.all()
    newNotify = Notifications.objects.filter(new=True)
    request.session['newNotify'] = len(newNotify)
    notify = notify[:len(notify)-len(newNotify)]
    context = {
        'newProducts': products[len(products) - 20:],
        'favoriteProducts': products[0:20],
        'randomProduct': products[ran:ran + 20],
        'newNotify': reversed(newNotify),
        'notify':reversed(notify),
    }
    if request.is_ajax():
        return render(request, 'Home/notify_comment.html', context)
    return render(request, 'Home/home.html', context)


# components
def form1(request):
    return render(request, 'components/form-1.html')
