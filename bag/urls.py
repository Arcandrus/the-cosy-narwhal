from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/<str:item_id>/', views.add_to_bag, name='add_to_bag'),
    path('remove/<str:product_code>/', views.remove_from_bag, name='remove_from_bag'),
]