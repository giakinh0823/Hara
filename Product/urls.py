from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('products/', views.products, name='products', ),
    path('products/<slug:slug>/', views.productDetail, name='product_detail', ),
    path('getdata/', views.getData, name='getData'),
    path('category/<slug:slug>/', views.category, name='category'),
    path('groupCategory/<slug:slug>/', views.groupCategory, name='group_category'),
    path('product/create', views.create_product, name='create_product'),
    path('product/edit', views.edit_product, name='edit_product'),
    path('product/edit/<slug:slug>/', views.edit_product_detail, name='edit_product_detail'),
    path('product/info', views.info_product, name='info_product'),
    path('checkout/<slug:slug>/', views.CreateCheckoutSessionView.as_view(), name="checkout"),
    path('loading/<slug:slug>/', views.loading, name="checkout_loading"),
    path('success/<slug:slug>/', views.success, name="checkout_success"),
    path('checkout/error/', views.error, name="checkout_error"),
    path('cancel/', views.cancel, name="checkout_cancel"),
    path('done/', views.done, name="checkout_done"),
]
