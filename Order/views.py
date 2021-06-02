from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail

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
        my_order.state = State.objects.get(slug="success")
        my_order.is_complete = True
        my_order.save()
        return JsonResponse({
            "user": str(my_order.user.username),
            "person": str(my_order.person.username),
            "product": my_order.product.title,
            "link": "/invest",
            "text": my_order.product.title,
        })


def cancel_order(request):
    if request.is_ajax():
        id = request.GET["id"]
        my_order = Order.objects.get(id=id)
        my_order.state = State.objects.get(slug="cancel")
        my_order.is_complete = False
        my_order.save()
        return JsonResponse({
            "user": str(my_order.user.username),
            "person": str(my_order.person.username),
            "product": my_order.product.title,
            "link": "/invest",
            "text": my_order.product.title,
        })


def accept_order(request):
    if request.is_ajax():
        id = request.GET["id"]
        my_order = Order.objects.get(id=id)
        my_order.state = State.objects.get(slug="waiting")
        my_order.save()
        return JsonResponse({
            "user": str(my_order.user.username),
            "person": str(my_order.person.username),
            "product": my_order.product.title,
            "link": "/invest",
            "text": my_order.product.title,
        })


def invest(request):
    orders = Order.objects.filter(person=request.user)
    notify = Notifications.objects.filter(user=request.user)
    notifyOrder = Notifications.objects.filter(user=request.user)
    for item in notifyOrder:
        if not item.link.find('invest') == -1:
            item.new = False
            item.save()
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


@login_required
def complain(request, slug):
    product = Product.objects.get(slug=slug)
    if request.is_ajax():
        email = request.POST["email"]
        content = request.POST["content"]
        send_mail("Report product - " + str(product.title), "Sản phẩm của bạn đã bị khiếu nại. "
                                                            "\nBạn có thể bị đình chỉ vĩnh viễn nếu như chúng tôi xác thực chính xác điều này"
                                                            "\nĐiều này dẫn đến việc bạn vi phạm chính sách của chúng tôi và chúng tôi sẽ mời các cơ quan tổ chức vào giải quyết."
                                                            "\nXin liên hệ với chúng tôi để biết thêm chi tiết."
                                                            "\nChúng tôi sẽ giải quyết mọi vấn đề qua địa chỉ email: giakinhfullstack@gmail.com"
                                                            "\nXin cảm ơn"
                                                            "\nDear, Hara",
                  'giakinhfullstack@gmail.com',
                  [product.user.email])
        send_mail("Report product - " + str(product.title), "Chúng tôi đã nhận được đơn khiếu nại của bạn về sản phẩm " + product.title + ""
                                                            "\nBạn xin vui lòng cung cấp các hình ảnh và thông tin rõ ràng bằng việc trả lời mail này."
                                                            "\nThông tin bao gồm hóa đơn, tin nhắn, và các thông tin về sản phẩm, lịch sử giao dịch, lịch sử order sản phẩm"
                                                            "\nChúng tôi sẽ xem xét về thông tin của bạn kỹ lưỡng và giúp bạn hoàn lại số tiền của bạn."
                                                            "\nXin cảm ơn."
                                                            "\nDear, Hara",
                  'giakinhfullstack@gmail.com',
                  [email])
        send_mail("Report product - " + str(product.title), str(content + " \nFrom email: " + email),
                  'giakinhfullstack@gmail.com',
                  ['giakinhfullstack@gmail.com'])
        return JsonResponse({"success": "success"})
    return render(request, 'Order/complain.html', {"product": product})
