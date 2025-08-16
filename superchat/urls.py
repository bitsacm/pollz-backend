from django.urls import path
from . import views

urlpatterns = [
    path('create-order/', views.create_order, name='create_order'),
    path('razorpay-webhook/', views.razorpay_webhook, name='razorpay_webhook'),
    path('get-super-chats/', views.get_super_chats, name='get_super_chats'),
]