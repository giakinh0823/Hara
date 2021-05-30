from django.shortcuts import render
from Product.models import *
from Register.models import *
# Create your views here.
import random


def home(request):
    products = Product.objects.all()
    ran = random.randint(1, len(products) - 20)
    context = {
        'newProducts': products[len(products) - 20:],
        'favoriteProducts': products[0:20],
        'randomProduct': products[ran:ran + 20],
    }
    if request.user.is_authenticated:
        notify = Notifications.objects.filter(user=request.user)
        newNotify = Notifications.objects.filter(new=True, user=request.user)
        favorites = Favorite.objects.filter(user=request.user)
        for product in products:
            product.favorite = False
            for favorite in favorites:
                if product == favorite.product:
                    product.favorite = True
                    break
        if notify or newNotify:
            request.session['newNotify'] = len(newNotify)
            notify = notify[:len(notify) - len(newNotify)]
            notify = reversed(notify)
            if not newNotify or len(newNotify) == 0:
                newNotify = None
            else:
                newNotify = reversed(newNotify)
            context = {
                'newProducts': products[len(products) - 20:],
                'favoriteProducts': products[0:20],
                'randomProduct': products[ran:ran + 20],
                'newNotify': newNotify,
                'notify': notify,
            }
        if request.is_ajax():
            return render(request, 'Home/notify_comment.html', context)
    return render(request, 'Home/home.html', context)


# components
def form1(request):
    return render(request, 'components/form-1.html')



def handler404(request,exception):
    return render(request, '404.html', status=404)

def handler500(request, *args, **argv):
    return render(request, '500.html', status=500)
