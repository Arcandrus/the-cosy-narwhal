from django.contrib import admin
from .models import Product, Color


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "color",
        "price",
        "rating",
        "image",
        "inventory",
    )

    ordering = ("code",)

class ColorAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
    )

    ordering = ("pk",)

admin.site.register(Product, ProductAdmin)
admin.site.register(Color, ColorAdmin)