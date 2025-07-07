from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from product.models import Product


def format_color_name(color_name):
    if not color_name:
        return ''
    # Replace underscores with spaces and title-case each word
    return color_name.replace('_', ' ').title()


def view_bag(request):
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    quantity = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url')

    try:
        product = Product.objects.get(code=item_id)
    except Product.DoesNotExist:
        messages.error(request, "Sorry, that product does not exist.")
        return redirect('home') 

    color = format_color_name(product.color.name) if product.color else "N/A"
    size = product.get_size_display() if hasattr(product, 'get_size_display') else "N/A"

    bag = request.session.get('bag', {})

    if item_id in bag:
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    request.session['bag'] = bag

    messages.success(request, f"Added {product.name} (Color: {color}, Size: {size}) to your bag.")

    return redirect(redirect_url)


def remove_from_bag(request, product_code):
    bag = request.session.get('bag', {})

    if product_code in bag:
        product = get_object_or_404(Product, code=product_code)
        formatted_color = format_color_name(product.color.name) if product.color else ''
        size_display = product.get_size_display() if product.size is not None else ''

        messages.success(
            request,
            f"Removed all {product.name} "
            + (f"({formatted_color}) " if formatted_color else "")
            + (f"Size {size_display} " if size_display else "")
            + "from your bag."
        )
        del bag[product_code]
    else:
        messages.error(request, "That item was not in your bag.")

    request.session['bag'] = bag
    return redirect('view_bag')