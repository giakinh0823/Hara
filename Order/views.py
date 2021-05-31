from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from Order.models import Order, State
from Product.models import Product
from Register.models import Notifications, Profile


@login_required
def order(request):
    productFavorites = Product.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    if productFavorites:
        productFavorites = productFavorites[len(productFavorites) - 7:]
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
        'orders': orders,
        'productFavorites': productFavorites,
        'profile': profile
    }
    return render(request, 'order/order.html', context)


def active_order(request):
    if request.is_ajax():
        id = request.GET["id"]
        my_order = Order.objects.get(id=id)
        if my_order.is_active:
            my_order.is_active = False
        else:
            my_order.is_active = True
        my_order.save()
        return JsonResponse({"data": "Is active"})

def success_order(request):
    if request.is_ajax():
        id = request.GET["id"]
        my_order = Order.objects.get(id=id)
        my_order.state = State.objects.get(name="success")
        my_order.is_complete = True
        my_order.save()
        return JsonResponse({
            "user": str(my_order.user.username),
            "person": str(my_order.person.username),
            "product": my_order.product.title,
            "link": my_order.product.get_absolute_url(),
            "text": my_order.product.title,
        })

def cancel_order(request):
    if request.is_ajax():
        id = request.GET["id"]
        my_order = Order.objects.get(id=id)
        my_order.state = State.objects.get(name="cancel")
        my_order.is_complete = False
        my_order.save()
        return JsonResponse({
            "user": str(my_order.user.username),
            "person": str(my_order.person.username),
            "product": my_order.product.title,
            "link": my_order.product.get_absolute_url(),
            "text": my_order.product.title,
        })

def accept_order(request):
    if request.is_ajax():
        id = request.GET["id"]
        my_order = Order.objects.get(id=id)
        my_order.state = State.objects.get(name="waiting")
        my_order.save()
        return JsonResponse({
            "user": str(my_order.user.username),
            "person": str(my_order.person.username),
            "product": my_order.product.title,
            "link": my_order.product.get_absolute_url(),
            "text": my_order.product.title,
        })

def invest(request):
    orders = Order.objects.filter(person=request.user)
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
        'newNotify': newNotify,
        'notify': notify,
        "orders": orders,
    }
    return render(request, 'Order/invest.html', context)