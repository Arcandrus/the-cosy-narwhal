from django.contrib import admin
from .models import Product, Color


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "price",
        "rating",
        "image",
        "inventory",
    )

    ordering = ("code",)

admin.site.register(Product, ProductAdmin)
admin.site.register(Color)