from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout_view, name='checkout'),
    path('success/<str:order_number>/', views.checkout_success, name='checkout_success'),
    path('save_order/', views.save_order, name='save_order'),
    path('orders/<str:order_number>/', views.order_detail, name='order_detail'),
]