from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from Order.models import Order
from Product.models import Product
from Register.models import Notifications, Profile


@login_required
def order(request):
    productFavorites = Product.objects.filter(user=request.user)
    profile = Profile.objects.get(user = request.user)
    if productFavorites:
        productFavorites = productFavorites[len(productFavorites)-7:]
    orders = Order.objects.filter(user=request.user)
    notifyOrder = Notifications.objects.filter(user=request.user)
    for item in notifyOrder:
        if not item.link.find('order') == -1:
            item.new = False
            item.save()
    newNotify = Notifications.objects.filter(new=True, user=request.user)
    notify = notifyOrder[:len(notifyOrder) - len(newNotify)]
    request.session['newNotify'] = len(newNotify)
    if notify or newNotify:
        request.session['newNotify'] = len(newNotify)
        notify = notify[:len(notify) - len(newNotify)]
        notify = reversed(notify)
        if not newNotify or len(newNotify) == 0:
            newNotify = None
        else:
            newNotify = reversed(newNotify)
    context = {
        'newNotify': newNotify,
        'notify': notify,
        'orders':orders,
        'productFavorites':productFavorites,
        'profile': profile
    }
    return render(request, 'order/order.html', context)
