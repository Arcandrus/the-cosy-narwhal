import stripe
import json
from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product
from profiles.forms import DeliveryInfoForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from .models import Order
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse


stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout_view(request):
    print("Checkout view called with method:", request.method)
    bag = request.session.get('bag', {})
    profile = request.user.profile

    # Build order summary & total price
    order_items = []
    total_price = 0
    for code, qty in bag.items():
        try:
            product = Product.objects.get(code=code)
            line_total = product.price * qty
            total_price += line_total
            order_items.append({
                'product': product,
                'quantity': qty,
                'line_total': line_total,
            })
        except Product.DoesNotExist:
            continue

    user_email = request.user.email

    if request.method == 'POST':
        form = DeliveryInfoForm(request.POST, instance=profile, user_email=user_email)
        if form.is_valid():
            form.save()

            # Create Stripe PaymentIntent
            try:
                intent = stripe.PaymentIntent.create(
                    amount=int(total_price * 100),  # amount in pence
                    currency='gbp',
                    metadata={'user_id': request.user.id},
                )
            except Exception as e:
                messages.error(request, f"Payment initialization error: {e}")
                form = DeliveryInfoForm(instance=profile, user_email=user_email)  # reset form
                return render(request, 'checkout/checkout.html', {
                    'order_items': order_items,
                    'total_price': total_price,
                    'form': form,
                    'bag_json': json.dumps(bag),
                })

            context = {
                'order_items': order_items,
                'total_price': total_price,
                'form': form,
                'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                'client_secret': intent.client_secret,
                'payment_phase': True,
                'bag_json': json.dumps(bag),
            }
            return render(request, 'checkout/checkout.html', context)
    else:
        print("Handling GET")
        print("Profile:", profile)
        print("Profile full_name:", profile.full_name)
        # GET request — just show the form with prepopulated profile data
        form = DeliveryInfoForm(instance=profile, user_email=user_email)

    return render(request, 'checkout/checkout.html', {
        'order_items': order_items,
        'total_price': total_price,
        'form': form,
        'bag_json': json.dumps(bag),
    })

@login_required
def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    # Optional: you can clear the bag here if you haven't done it before
    request.session['bag'] = {}
    request.session.pop('order_data', None)  # clear if exists, no error if not

    # Build order items to show nicely
    order_items = []
    for code, qty in order.items.items():
        try:
            product = Product.objects.get(code=code)
            order_items.append({
                'product': product,
                'quantity': qty,
                'line_total': product.price * qty,
            })
        except Product.DoesNotExist:
            continue

    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'checkout/checkout_success.html', context)


@csrf_protect
@login_required
def save_order(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    try:
        data = json.loads(request.body)
        bag = data.get('items')
        total_price = data.get('total_price')
    except Exception:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    if not bag or total_price is None:
        return JsonResponse({'error': 'Invalid order data'}, status=400)

    # Example: if items is JSONField
    try:
        order = Order.objects.create(
            user=request.user,
            items=bag,  # store dict directly if JSONField
            total_price=total_price,
        )
    except Exception as e:
        return JsonResponse({'error': f'Failed to save order: {str(e)}'}, status=500)

    # Clear the bag session data
    request.session['bag'] = {}
    request.session.save()

    # Return a safe fallback for order_number
    order_number = getattr(order, 'order_number', order.pk)

    return JsonResponse({'status': 'success', 'order_number': order_number})


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    item_data = order.items  # this is your stored dictionary
    item_list = []

    for code, qty in item_data.items():
        try:
            product = Product.objects.get(code=code)
            item_list.append({
                'product': product,
                'quantity': qty,
                'line_total': product.price * qty,
            })
        except Product.DoesNotExist:
            continue  # or handle missing product more explicitly

    context = {
        'order': order,
        'item_list': item_list,
    }
    return render(request, 'checkout/order_detail.html', context)