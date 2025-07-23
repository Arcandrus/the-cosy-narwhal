from django.urls import path
from . import views

urlpatterns = [
    path("", views.all_products, name="products"),
    path("<int:product_id>/", views.product_detail, name="product_detail"),
    path("product_management", views.product_management, name="product_management"),
    path('add/', views.add_product, name='add_product'), 
    path('edit/', views.edit_product, name='edit_product'),
    path('remove/', views.remove_product, name='remove_product'),
    path('inventory/', views.update_inventory, name='update_inventory'),
    path('sales/', views.sales, name='sales'),
]