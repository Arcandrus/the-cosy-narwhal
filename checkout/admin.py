from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'total_price', 'created_at', 'updated_at')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    search_fields = ('order_number', 'user', 'created_at')
    ordering = ('-created_at',)