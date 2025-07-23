from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Product
from .forms import ReviewForm
from django.contrib.auth.decorators import user_passes_test
from .forms import ProductForm
from django.db import models
from django.contrib import messages
from .forms import ProductInventoryFormSet
from checkout.models import Order
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict
from decimal import Decimal

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

    prefix = product.code[:3]
    variant_products = Product.objects.filter(code__startswith=prefix).order_by('id')

    # Build color_links
    color_links = []
    for color in product.available_colors.all():
        variant = variant_products.filter(color=color).first()
        if variant:
            color_links.append((color.name.lower(), variant.id))
    color_links.sort(key=lambda x: x[0])

    # Build size_links
    size_links = []
    for size_value, size_label in Product.SIZE:
        if size_value == product.size:
            continue
        variant = variant_products.filter(size=size_value, color=product.color).first()
        if variant:
            size_links.append((size_value, size_label, variant.id))

    reviews = product.reviews.all().order_by('-created_at')

    # ✅ Check if user can leave a review
    can_review = False
    if request.user.is_authenticated:
        already_reviewed = reviews.filter(user=request.user).exists()

        if not already_reviewed:
            user_orders = Order.objects.filter(user=request.user)
            for order in user_orders:
                if product.code in order.items:
                    can_review = True
                    break

    # Only accept POST if allowed
    if request.method == 'POST' and can_review:
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
        'can_review': can_review,
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


@user_passes_test(is_superuser)
def update_inventory(request):
    queryset = Product.objects.all()

    if request.method == 'POST':
        formset = ProductInventoryFormSet(request.POST, queryset=queryset)

        print("POST received!")
        print("Raw POST data:", request.POST)

        if formset.is_valid():
            print("Formset is valid.")
            formset.save()
            messages.success(request, "Inventory successfully updated.")
            return redirect('product_management')
        else:
            print("Formset errors:", formset.errors)
    else:
        formset = ProductInventoryFormSet(queryset=queryset)

    return render(request, 'product/inventory.html', {
        'formset': formset,
    })


@user_passes_test(is_superuser)
def sales(request):
    # Get filter period from query params, default to 7 days
    period = request.GET.get('period', '7')
    sort = request.GET.get('sort', 'most_sales')  # get sorting option, default to most_sales
    now = timezone.now()

    if period == '1':
        start_date = now - timedelta(days=1)
    elif period == '7':
        start_date = now - timedelta(days=7)
    elif period == '30':
        start_date = now - timedelta(days=30)
    else:  # 'all' or invalid value
        start_date = None

    if start_date:
        orders = Order.objects.filter(created_at__gte=start_date)
    else:
        orders = Order.objects.all()

    # Aggregate total units sold per product code
    sales_data = defaultdict(int)
    for order in orders:
        for code, qty in order.items.items():
            sales_data[code] += qty

    # Build product sales info
    products_sales = []
    total_sales = Decimal('0.00')  # initialize total

    product_codes = sales_data.keys()
    products = Product.objects.filter(code__in=product_codes)
    products_map = {p.code: p for p in products}

    for code, qty_sold in sales_data.items():
        product = products_map.get(code)
        if not product:
            continue  # product deleted

        subtotal = qty_sold * product.price
        total_sales += subtotal

        products_sales.append({
            'image': product.image.url if product.image else None,
            'code': product.code,
            'name': product.name,
            'units_sold': qty_sold,
            'price': product.price,
            'subtotal': subtotal,
            'inventory': product.inventory,
        })

    # Sorting logic
    if sort == 'most_sales':
        products_sales.sort(key=lambda x: x['units_sold'], reverse=True)
    elif sort == 'highest_subtotal':
        products_sales.sort(key=lambda x: x['subtotal'], reverse=True)
    elif sort == 'lowest_stock':
        products_sales.sort(key=lambda x: x['inventory'])
    elif sort == 'price_high_to_low':
        products_sales.sort(key=lambda x: x['price'], reverse=True)
    elif sort == 'price_low_to_high':
        products_sales.sort(key=lambda x: x['price'])
    else:
        # default fallback sort
        products_sales.sort(key=lambda x: x['units_sold'], reverse=True)

    context = {
        'products_sales': products_sales,
        'selected_period': period,
        'selected_sort': sort,  # pass the selected sort for template to highlight dropdown
        'total_sales': total_sales,
    }

    return render(request, 'product/sales.html', context)
