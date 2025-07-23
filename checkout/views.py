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
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from the_cosy_narwhal.utils import calculate_delivery


stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout_view(request):
    print("Checkout view called with method:", request.method)
    bag = request.session.get('bag', {})

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

    delivery_charge, delivery_type, grand_total = calculate_delivery(order_items)
    
    # Authenticated user data (if available)
    profile = None
    user_email = ''
    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)
        user_email = request.user.email

    if request.method == 'POST':
        form = DeliveryInfoForm(request.POST, instance=profile, user_email=user_email)
        if form.is_valid():
            # Capture the save_info checkbox value ('on' if checked)
            save_info = request.POST.get('save_info') == 'on'

            # Save delivery info in session
            delivery_data = form.cleaned_data
            request.session['delivery_info'] = {
                'email': delivery_data.get('email'),
                'full_name': delivery_data.get('full_name', ''),
                'street_address1': delivery_data.get('street_address1', ''),
                'street_address2': delivery_data.get('street_address2', ''),
                'town_or_city': delivery_data.get('town_or_city', ''),
                'county': delivery_data.get('county', ''),
                'postcode': delivery_data.get('postcode', ''),
                'country': delivery_data.get('country', ''),
            }
            request.session['save_info'] = save_info
            request.session.modified = True
            # Create Stripe PaymentIntent
            try:
                metadata = {}
                if request.user.is_authenticated:
                    metadata['user_id'] = request.user.id

                intent = stripe.PaymentIntent.create(
                    amount=int(total_price * 100),
                    currency='gbp',
                    metadata=metadata,
                )
            except Exception as e:
                form.add_error(None, f"Payment initialization error: {e}")
                return render(request, 'checkout/checkout.html', {
                    'order_items': order_items,
                    'total_price': total_price,
                    'delivery_charge': delivery_charge,
                    'delivery_type': delivery_type,
                    'grand_total': grand_total,
                    'form': form,
                    'bag_json': json.dumps(bag),
                    'delivery_info': request.session.get('delivery_info', {}),
                    'save_info': request.session.get('save_info', True),
                })

            return render(request, 'checkout/checkout.html', {
                'order_items': order_items,
                'total_price': total_price,
                'delivery_charge': delivery_charge,
                'delivery_type': delivery_type,
                'grand_total': grand_total,
                'form': form,
                'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                'client_secret': intent.client_secret,
                'payment_phase': True,
                'bag_json': json.dumps(bag),
                'delivery_info': request.session.get('delivery_info', {}),
                'save_info': request.session.get('save_info', True),
            })
    else:
        form = DeliveryInfoForm(instance=profile, user_email=user_email)

    return render(request, 'checkout/checkout.html', {
        'order_items': order_items,
        'total_price': total_price,
        'delivery_charge': delivery_charge,
        'delivery_type': delivery_type,
        'grand_total': grand_total,
        'form': form,
        'bag_json': json.dumps(bag),
        'delivery_info': request.session.get('delivery_info', {}),
        'save_info': request.session.get('save_info', True),
    })


def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    
    # Decrement inventory for each product in the order
    for code, qty in order.items.items():
        try:
            product = Product.objects.get(code=code)
            product.inventory = max(product.inventory - qty, 0)  # Prevent negative inventory
            product.save()
        except Product.DoesNotExist:
            # Optionally log this or handle missing product case
            continue

    request.session['bag'] = {}
    request.session.pop('order_data', None)

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

    delivery_charge, delivery_type, total_with_delivery = calculate_delivery(order_items)

    context = {
        'order': order,
        'order_items': order_items,
        'delivery_charge': delivery_charge,
        'delivery_type': delivery_type,
        'total_with_delivery': total_with_delivery,
    }

    return render(request, 'checkout/checkout_success.html', context)


@csrf_protect
def save_order(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    try:
        data = json.loads(request.body)
        bag = data.get('items')
        total_price = data.get('total_price')

        # Get delivery info
        email = data.get('email')
        full_name = data.get('full_name')
        street_address1 = data.get('street_address1')
        street_address2 = data.get('street_address2', '')
        town_or_city = data.get('town_or_city')
        county = data.get('county', '')
        postcode = data.get('postcode')
        country = data.get('country')
        save_info = data.get('save_info', True)  # Defaults to True if not sent
    except Exception:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    if not bag or total_price is None:
        return JsonResponse({'error': 'Invalid order data'}, status=400)

    user = request.user if request.user.is_authenticated else None

    # Save the order
    try:
        order = Order.objects.create(
            user=user,
            email=email,
            items=bag,
            total_price=total_price,
            full_name=full_name,
            street_address1=street_address1,
            street_address2=street_address2,
            town_or_city=town_or_city,
            county=county,
            postcode=postcode,
            country=country,
        )
    except Exception as e:
        return JsonResponse({'error': f'Failed to save order: {str(e)}'}, status=500)

    # Save delivery info to profile if requested and user is authenticated
    if save_info and user is not None:
        profile = getattr(user, 'profile', None)
        if profile:
            profile.full_name = full_name
            profile.street_address1 = street_address1
            profile.street_address2 = street_address2
            profile.town_or_city = town_or_city
            profile.county = county
            profile.postcode = postcode
            profile.country = country
            profile.save()
    else:
        print("DEBUG: Not saving profile info or user not authenticated")

    # Build order items for email and delivery calculation
    order_items = []
    for code, qty in bag.items():
        try:
            product = Product.objects.get(code=code)
            line_total = product.price * qty
            order_items.append({
                'product': product,
                'quantity': qty,
                'line_total': line_total,
            })
        except Product.DoesNotExist:
            continue

    # Calculate delivery charge, type, and grand total
    delivery_charge, delivery_type, grand_total = calculate_delivery(order_items)

    try:
        context = {
            'order_number': order.order_number,
            'full_name': full_name,
            'street_address1': street_address1,
            'street_address2': street_address2,
            'town_or_city': town_or_city,
            'county': county,
            'postcode': postcode,
            'country': country,
            'order_items': order_items,
            'delivery_charge': delivery_charge,
            'total': grand_total,
        }
        message = render_to_string('emails/conf_email.txt', context)
        subject = f'The Cosy Narwhal - Order Number {order.order_number}'

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )
    except Exception as e:
        print("Failed to send confirmation email:", e)

    # Clear bag
    request.session['bag'] = {}
    request.session.save()

    return JsonResponse({'status': 'success', 'order_number': getattr(order, 'order_number', order.pk)})

@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    item_data = order.items  # stored dictionary of items in the bag
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
            continue

    # Calculate delivery charge, type, and grand total
    delivery_charge, delivery_type, grand_total = calculate_delivery(item_list)

    context = {
        'order': order,
        'item_list': item_list,
        'delivery_charge': delivery_charge,
        'delivery_type': delivery_type,
        'grand_total': grand_total,
    }
    return render(request, 'checkout/order_detail.html', context)