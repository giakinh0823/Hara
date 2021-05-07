from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('products/', views.products, name='products',),
    path('products/<slug:slug>/', views.productDetail, name='product_detail',),
    path('getdata/',views.getData, name='getData'),
    path('category/<slug:slug>/', views.category, name='category'),
    path('groupCategory/<slug:slug>/', views.groupCategory, name='group_category'),
    path('product/create', views.create_product, name='create_product')
]