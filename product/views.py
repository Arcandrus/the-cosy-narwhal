from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product


def all_products(request):
    query = request.GET.get('q', '')
    all_products = Product.objects.order_by('code', 'id')

    if query:
        # Search: show all matching with full product names (no trimming)
        all_products = all_products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        products_to_show = all_products
        for product in products_to_show:
            product.display_name = product.name  # full name with variant info
    else:
        # No search: show unique prefixes with trimmed names
        seen_prefixes = set()
        unique_products = []
        for product in all_products:
            prefix = product.code[:3]
            if prefix not in seen_prefixes:
                if '-' in product.name:
                    product.display_name = product.name.split('-')[0].strip()
                else:
                    product.display_name = product.name
                unique_products.append(product)
                seen_prefixes.add(prefix)
        products_to_show = unique_products

    context = {
        'products': products_to_show,
        'search_term': query,
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

    color_links.sort(key=lambda x: x[0])
    
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

