from django.contrib import admin
from .models import Product, Color, Review


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
    list_filter = ('rating', 'color', 'inventory')
    search_fields = ('code', 'name')

    ordering = ("code",)

class ColorAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
    )

    ordering = ("pk",)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'text')
    ordering = ('-created_at',)


admin.site.register(Review)
admin.site.register(Product, ProductAdmin)
admin.site.register(Color, ColorAdmin)