from django.shortcuts import render, get_object_or_404
from .models import Product


def all_products(request):
    # Get all products ordered by code
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
    prefix = product.code[:3] 

    # Get all products that share the same prefix
    variant_products = Product.objects.filter(code__startswith=prefix).order_by('id')
        
    color_links = []
    for color in product.available_colors.all():
        variant = variant_products.filter(color=color).first()
        if variant:
            color_links.append((color.name.lower(), variant.id))

    SIZE_DICT = dict(Product.SIZE)
    size_links = []
    for size_value, size_label in Product.SIZE:
        if size_value == product.size:
            continue  # Skip current size
        variant = variant_products.filter(size=size_value, color=product.color).first()
        if variant:
            size_links.append((size_value, size_label, variant.id))

    context = {
        'product': product,
        'product_id_str': str(product.id),
        'color_links': color_links,
        'size_links': size_links,
    }
    
    return render(request, "product/product_detail.html", context)

