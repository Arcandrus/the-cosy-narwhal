from django.shortcuts import render, get_object_or_404
from .models import Product


def all_products(request):
    # Get all products ordered by code or id (whatever keeps the order consistent)
    all_products = Product.objects.order_by('code', 'id')

    # Use a set to track seen prefixes
    seen_prefixes = set()
    unique_products = []

    for product in all_products:
        prefix = product.code[:3]
        if prefix not in seen_prefixes:
            # Conditionally trim the product name at the hyphen
            if '-' in product.name:
                product.display_name = product.name.split('-')[0].strip()
            else:
                product.display_name = product.name
            unique_products.append(product)
            seen_prefixes.add(prefix)

    context = {
        'products': unique_products,
    }
    
    return render(request, 'product/product.html', context)



def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Extract the prefix (e.g., "WHA") from the product code
    prefix = product.code[:3]  # Assuming codes like WHA0001, WHA0002

    # Get all products that share the same prefix
    variant_products = Product.objects.filter(code__startswith=prefix).order_by('id')
    print(variant_products)

    for variant in variant_products:
        print(f"Product: {variant.name} (ID: {variant.id}), Color: {variant.color}")
        print("Available colors:", list(variant.available_colors.all()))
        
    color_links = []
    for color in product.available_colors.all():
        variant = variant_products.filter(color=color).first()
        if variant:
            color_links.append((color.name.lower(), variant.id))
    print(color_links)

    context = {
        'product': product,
        'product_id_str': str(product.id),
        'color_links': color_links,
    }
    
    return render(request, "product/product_detail.html", context)

