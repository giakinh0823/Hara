from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from django.core.mail import send_mail


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        print(user)
        print(user.email)
        if user.id:
            send_mail(
                'Đăng nhập website Hara',
                'Chúng tôi nhận thấy tài khoản của bạn đang hoạt động.',
                'giakinhfullstack@gmail.com',
                [str(user.email)],
            )
            return
        if not user.email:
            return

        try:
            user = User.objects.get(
                email=user.email)  # if user exists, connect the account to the existing account and login
            sociallogin.connect(request, user)
        except User.DoesNotExist:
            pass