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
    path('product/info/<slug:slug>/deleteVideo/<int:id>/', views.delete_video_product, name='delete_video_product'),
    path('product/info/<slug:slug>/deleteImage/<int:id>/', views.delete_image_product, name='delete_image_product'),
    path('product/info/newvideo/<int:id>/', views.new_info_video, name='new_info_video'),
    path('product/info/newInfoImage/<int:id>/', views.new_info_image, name='new_info_image'),
    path('product/info/<slug:slug>', views.info_product_detail, name='info_product_detail'),
    path('checkout/<slug:slug>/', views.CreateCheckoutSessionView.as_view(), name="checkout"),
    path('loading/<slug:slug>/', views.loading, name="checkout_loading"),
    path('success/<slug:slug>/', views.success, name="checkout_success"),
    path('checkout/error/', views.error, name="checkout_error"),
    path('cancel/', views.cancel, name="checkout_cancel"),
    path('done/', views.done, name="checkout_done"),
]
