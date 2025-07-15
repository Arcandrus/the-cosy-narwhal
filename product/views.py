from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Product
from .forms import ReviewForm
from django.contrib.auth.decorators import user_passes_test
from .forms import ProductForm
from django.db import models
from django.contrib import messages


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

    # Get all reviews for this product, newest first
    reviews = product.reviews.all().order_by('-created_at')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()

    context = {
        'product': product,
        'product_id_str': str(product.id),
        'color_links': color_links,
        'size_links': size_links,
        'reviews': reviews,
        'form': form,
    }
    
    return render(request, "product/product_detail.html", context)


def is_superuser(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(is_superuser)
def product_management(request):
    return render(request, 'product/product_management.html')

@user_passes_test(is_superuser)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            new_product = form.save()
            messages.success(request, f"'{new_product.name}' added successfully!")
            return redirect('product_management') 
    else:
        form = ProductForm()

    return render(request, 'product/add_product.html', {'form': form})


@user_passes_test(is_superuser)
def edit_product(request):
    products = Product.objects.all().order_by('name')  # full list for dropdown

    product = None
    form = None
    search_results = None

    # Get params
    product_id = request.GET.get('product_id')
    search_query = request.GET.get('search')

    # Load product to edit
    if product_id:
        product = get_object_or_404(Product, pk=product_id)
    elif search_query:
        # Get all matching products for search results
        search_results = Product.objects.filter(
            models.Q(code__icontains=search_query) | 
            models.Q(name__icontains=search_query)
        ).order_by('name')
        # Select first matching product to edit (optional)
        product = search_results.first()

    if request.method == 'POST':
        product_id_post = request.POST.get('product_id')
        product = get_object_or_404(Product, pk=product_id_post)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            messages.success(request, f'{product.name} Updated Successfully')
            form.save()
            return redirect(f"{request.path}?product_id={product.id}")
        else:
            print(form.errors)
    else:
        if product:
            form = ProductForm(instance=product)

    context = {
        'products': products,
        'form': form,
        'selected_product': product,
        'search_query': search_query,
        'search_results': search_results,
    }

    return render(request, 'product/edit_product.html', context)


@user_passes_test(is_superuser)
def remove_product(request):
    products = Product.objects.all().order_by('name')
    search_query = request.GET.get('search')
    product_to_delete = None
    search_results = []

    if search_query:
        search_results = Product.objects.filter(
            models.Q(code__icontains=search_query) | models.Q(name__icontains=search_query)
        )

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_to_delete = get_object_or_404(Product, pk=product_id)
        product_to_delete.delete()
        messages.success(request, f"Product '{product_to_delete.name}' was removed successfully.")
        return redirect('remove_product')

    context = {
        'products': products,
        'search_query': search_query,
        'search_results': search_results,
    }
    return render(request, 'product/remove_product.html', context)