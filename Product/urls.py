from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('products/', views.products, name='products',),
    path('products/<slug:slug>/', views.productDetail, name='product_detail',),
    path('getdata/',views.getData, name='getData'),
    path('category/<slug:slug>/', views.category, name='category'),
    path('groupCategory/<slug:slug>/', views.groupCategory, name='group_category'),
    path('product/create', views.create_product, name='create_product'),
    path('checkout/<slug:slug>/', views.CreateCheckoutSessionView.as_view(), name="checkout"),
    path('success/', views.success, name="checkout_success"),
    path('checkout/error/', views.error, name="checkout_error"),
    path('cancel/', views.cancel, name="checkout_cancel"),
]